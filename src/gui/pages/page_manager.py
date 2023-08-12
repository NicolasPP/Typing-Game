from typing import Type

from gui.pages.page import Page


class PageManager:

    def __init__(self) -> None:
        self.pages: dict[str, Page] = {}
        self.current_page: str | None = None

    def add_page(self, page: Type[Page]) -> None:
        self.pages[page.__name__] = page(self.set_page)

    def get_page(self) -> Page:
        assert self.current_page is not None, "current page not set"
        assert self.current_page in self.pages, f"current page {self.current_page} does not exist"
        return self.pages[self.current_page]

    def set_page(self, page: str) -> None:
        assert page in self.pages, f"current page {self.current_page} does not exist"
        self.current_page = page
