from __future__ import annotations

"""High‑level Rutube API client.

This module provides a thin wrapper around the Rutube web UI that automates
getting an authenticated :class:`requests.Session`, creating a live stream and
optionally uploading a thumbnail.  It hides low‑level Selenium details behind a
simple, synchronous interface so that calling code can treat Rutube like a
regular REST service.

Example
-------
>>> client = RutubeClient("user@example.com", "hunter2")
>>> info = client.schedule_stream(
...     title="Моя трансляция",
...     description="Сегодня играем в Factorio!",
...     thumbnail_path="preview.jpg",
... )
>>> print(info.url, info.stream_key)
"""

from dataclasses import dataclass
from pathlib import Path
import json
import os
import pickle
import time
from typing import Final, Iterable, Tuple

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

__all__ = ["RutubeClient", "StreamInfo"]


@dataclass
class StreamInfo:
    """Returned by :pymeth:`RutubeClient.schedule_stream`."""

    url: str
    stream_key: str
    video_id: str

    def as_tuple(self) -> Tuple[str, str]:
        return self.url, self.stream_key


class RutubeAuthError(RuntimeError):
    """Raised if we fail to authenticate with Rutube."""


class RutubeClient:
    """Imperative synchronous Rutube client.

    The client maintains its own :class:`requests.Session` with valid cookies.
    If the cookies have expired it automatically refreshes them via Selenium.
    """

    _LOGIN_URL: Final[str] = "https://rutube.ru/multipass/login/"
    _PROFILE_URL: Final[str] = "https://studio.rutube.ru/multipass/api/accounts/profile"
    _STREAM_CREATE_URL: Final[str] = "https://studio.rutube.ru/api/v2/video/create/stream/"
    _STREAM_DETAILS_URL_TMPL: Final[str] = "https://studio.rutube.ru/api/v2/video/stream/{video_id}"
    _THUMBNAIL_UPLOAD_URL_TMPL: Final[str] = "https://studio.rutube.ru/api/video/{video_id}/thumbnail/?client=vulp"

    _COOKIES_FILE: Final[Path] = Path.home() / ".rutube_cookies.pkl"

    def __init__(self, login: str, password: str) -> None:
        self._login = login
        self._password = password
        self._session: requests.Session | None = None

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def schedule_stream(
        self,
        title: str,
        description: str = "",
        *,
        thumbnail_path: str | os.PathLike | None = None,
        category: int = 6,
        is_adult: bool = False,
        is_hidden: bool = False,
    ) -> StreamInfo:
        """Create a new stream and (optionally) upload a thumbnail."""

        session = self._get_session()
        video_id = self._create_stream(
            session,
            title,
            description,
            category=category,
            is_adult=is_adult,
            is_hidden=is_hidden,
        )
        details = self._get_stream_details(session, video_id)

        if thumbnail_path is not None:
            self._upload_thumbnail(session, video_id, thumbnail_path)

        return StreamInfo(url=details[0], stream_key=details[1], video_id=video_id)

    # ---------------------------------------------------------------------
    # Private helpers – Session management
    # ---------------------------------------------------------------------
    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._ensure_valid_cookies(self._session)
        return self._session

    def _ensure_valid_cookies(self, session: requests.Session) -> None:
        """Load cookies from disk or perform login if needed."""

        cookies = self._load_cookies()
        if cookies:
            _inject_cookies(session, cookies)
            if session.get(self._PROFILE_URL).ok:
                return  # cookies still valid

        # Need fresh cookies – go through Selenium login flow.
        new_cookies = self._selenium_login()
        _inject_cookies(session, new_cookies)
        self._save_cookies(new_cookies)

        if not session.get(self._PROFILE_URL).ok:
            raise RutubeAuthError("Failed to authenticate after refreshing cookies.")

    # ------------------------------------------------------------------
    # Selenium login flow
    # ------------------------------------------------------------------
    def _selenium_login(self) -> Iterable[dict]:
        """Automate the Rutube login page and return fresh cookies."""

        options = Options()
        # options.add_argument("--headless=new")  # comment‑out for debugging
        options.add_argument("--disable‑blink‑features=AutomationControlled")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 30)
        driver.get(self._LOGIN_URL)

        # 1. Enter login/email
        wait.until(EC.element_to_be_clickable((By.ID, "phone-or-email-login"))).send_keys(self._login)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 2. Enter password
        wait.until(EC.element_to_be_clickable((By.ID, "login-password"))).send_keys(self._password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 3. Wait for JWT cookie to appear
        for _ in range(50):  # ~15 seconds
            cookies = driver.get_cookies()
            if any(c["name"] == "jwt" for c in cookies):
                break
            time.sleep(0.3)
        else:
            driver.quit()
            raise RutubeAuthError("JWT cookie did not appear – incorrect credentials?")

        driver.quit()
        return cookies

    # ------------------------------------------------------------------
    # REST calls
    # ------------------------------------------------------------------
    def _create_stream(
        self,
        session: requests.Session,
        title: str,
        description: str,
        *,
        category: int,
        is_adult: bool,
        is_hidden: bool,
    ) -> str:
        """POST /video/create/stream – return video id."""

        payload = dict(
            stream_status="wait",
            title=title,
            description=description,
            category=category,
            push_auto_start=True,
            is_adult=is_adult,
            is_hidden=is_hidden,
        )
        resp = session.post(self._STREAM_CREATE_URL, json=payload, allow_redirects=False)
        resp.raise_for_status()
        return resp.json()["video"]

    def _get_stream_details(self, session: requests.Session, video_id: str) -> Tuple[str, str]:
        resp = session.get(self._STREAM_DETAILS_URL_TMPL.format(video_id=video_id))
        resp.raise_for_status()
        data = resp.json()
        return data["source_url"], data["input_key_gen"]

    def _upload_thumbnail(self, session: requests.Session, video_id: str, path: str | os.PathLike) -> None:
        with open(path, "rb") as fh:
            files = {"file": (Path(path).name, fh, "image/jpeg")}
            resp = session.post(self._THUMBNAIL_UPLOAD_URL_TMPL.format(video_id=video_id), files=files)
            resp.raise_for_status()

    # ------------------------------------------------------------------
    # Cookie helpers
    # ------------------------------------------------------------------
    @classmethod
    def _save_cookies(cls, cookies: Iterable[dict]) -> None:
        with open(cls._COOKIES_FILE, "wb") as fh:
            pickle.dump(list(cookies), fh)

    @classmethod
    def _load_cookies(cls) -> list[dict]:
        try:
            with open(cls._COOKIES_FILE, "rb") as fh:
                return pickle.load(fh)
        except FileNotFoundError:
            return []


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------

def _inject_cookies(session: requests.Session, cookies: Iterable[dict]) -> None:
    """Insert cookies into *session* exactly as Selenium provides them."""

    for c in cookies:
        session.cookies.set(
            c["name"],
            c["value"],
            domain=c.get("domain"),
            path=c.get("path", "/"),
        )