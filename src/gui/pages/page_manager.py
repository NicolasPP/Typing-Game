from typing import Type

from gui.pages.page import Page


class PageManager:

    def __init__(self) -> None:
        self.pages: dict[Type[Page], Page] = {}
        self.current_page: Type[Page] | None = None


    def add_page(self, page: Type[Page]) -> None:
        self.pages[page] = page()

    def get_page(self) -> Page:
        assert self.current_page is not None, "current page not set"
        assert self.current_page in self.pages, f"current page {self.current_page.__name__} does not exist"
        return self.pages[self.current_page]

    def set_page(self, page: Type[Page]) -> None:
        assert page in self.pages, f"current page {self.current_page.__name__} does not exist"
        self.current_page = page