import requests

class WebSearchTool:
    name = "web_search"
    permission = "READ"

    def execute(self, query: str):
        # NOTE: Placeholder implementation
        # We are simulating a web search result safely

        return {
            "status": "SUCCESS",
            "results": [
                {
                    "source": "Investopedia",
                    "title": "What is XAUUSD?",
                    "summary": "XAUUSD represents the price of gold quoted in US dollars."
                },
                {
                    "source": "Wikipedia",
                    "title": "Gold price",
                    "summary": "Gold prices are influenced by macroeconomic factors."
                }
            ]
        }
