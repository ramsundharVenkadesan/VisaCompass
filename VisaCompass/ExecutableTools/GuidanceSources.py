from langchain.tools import tool
from ExecutableTools.SearchTool import tavily_search_invocation, allowed_domains
import httpx
from bs4 import BeautifulSoup

@tool
async def search_dhs_data(query:str) -> str:
    """
    Searches Department of Homeland Security (DHS) databases and general immigration resources.

    Use this tool for broad immigration policy, enforcement, or operational questions that
    do not specifically fall under the USCIS Policy Manual or DOS Foreign Affairs Manual.

    Args:
        query (str): The specific search query regarding DHS operations, news, or broad policies.
    """
    return await tavily_search_invocation(query=query)

@tool
async def search_uscis_data(topic:str) -> str:
    """
    Searches the official USCIS Policy Manual for guidance, rules, and adjudicative guidelines.

    Use this tool to determine eligibility requirements, application procedures, and how
    USCIS officers make decisions on specific immigration benefits and petitions.

    Args:
        topic (str): The specific immigration topic, form, or benefit (e.g., "H-1B specialty occupation", "adjustment of status").
    """
    return await tavily_search_invocation(query=f"USCIS policy manual guidance on {topic}")

@tool
async def search_dos_stamping_data(topic:str) -> str:
    """
    Searches the Department of State's Foreign Affairs Manual (9 FAM) for visa and consular guidance.

    Use this tool for questions regarding visa issuance, passport stamping, consular processing,
    consular interviews, and visa refusals (like 221(g)).

    Args:
        topic (str): The specific visa category or consular processing issue (e.g., "F-1 student intent", "L-1 blanket").
    """
    return await tavily_search_invocation(query=f"Department of State 9 FAM visa {topic} guidance", extra_domains=["state.gov"])

@tool
async def get_immigration_lawyer_advice(topic:str) -> str:
    """
    Retrieves professional practice advisories, compliance rules, and legal defense strategies.

    Use this tool to find legal interpretations and best practices from reputable sources
    like the American Immigration Lawyers Association (AILA) and the Department of Justice (DOJ).

    Args:
        topic (str): The legal compliance issue, defense strategy, or case law topic (e.g., "categorical approach for convictions", "PERM audits").
    """
    return await tavily_search_invocation(query=f"immigration lawyer practice advisory compliance rules for {topic}", extra_domains=["aila.org", "justice.gov"])

@tool
async def crawl_dhs_data(url:str) -> str:
    """
    Crawls and extracts live textual content directly from an official U.S. government webpage.

    Use this tool when you already have a specific government URL (e.g., from a previous search)
    and need to read the exact text of a policy memo, press release, or specific webpage.
    Restricted to official U.S. government domains.

    Args:
        url (str): The exact, fully qualified URL of the official government page to scrape.
    """
    cleaned_url = url.strip()
    if not any(domain in cleaned_url for domain in allowed_domains):
        return f"Error: Crawling is restricted to official U.S. government domains"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(cleaned_url, headers=headers)
            response.raise_for_status()
            html_content = response.text

            soup = BeautifulSoup(html_content, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]): tag.decompose()
            main_node = soup.find("main") or soup.find("article") or soup.find("body")
            extracted_text = main_node.get_text(separator="\n", strip=True) if main_node else soup.get_text()

            lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]
            return f"Live Extracted Federal Content:\n" + "\n".join(lines[:100])
    except Exception as e: return f"Error: {str(e)}"
