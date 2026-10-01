from langchain.tools import tool
from ExecutableTools.SearchTool import tavily_search_invocation

@tool
async def search_gov_info(query:str) -> str:
    """
    Searches GovInfo and the Federal Register for proposed rules, final rules, and federal agency notices.

    Use this tool to discover federal regulatory actions, public notices, presidential documents,
    and general rulemaking history on a specific topic. This performs a broad textual search across
    federal publications.

    Args:
        query (str): The search query, keyword, or specific regulatory topic to look up (e.g., "H-1B wage levels", "EPA emissions standards proposed rule").
    """
    return await tavily_search_invocation(query=f"Federal Register GovInfo proposed and final rules for {query}",
                                    extra_domains=["govinfo.gov", "federalregister.gov"])

@tool
async def get_gov_info_package_summary(package_id:str) -> str:
    """
    Retrieves the summary and overarching metadata for a specific GovInfo package.

    In GovInfo terminology, a "package" represents an entire issue of a publication or a complete
    overarching document (e.g., an entire daily issue of the Federal Register). Use this tool when
    you have a known Package ID and need the high-level summary, publication date, and metadata
    for that specific issue.

    Args:
        package_id (str): The unique GovInfo identifier for the package (e.g., "FR-2023-01-15", "CREC-2018-10-10").
    """
    return await tavily_search_invocation(query=f"Federal Register GovInfo package summary for {package_id}",
                                    extra_domains=["govinfo.gov", "federalregister.gov"])

@tool
async def get_gov_info_granules(package_id:str) -> str:
    """
    Retrieves the details and specific granules contained within a GovInfo package.

    In GovInfo terminology, "granules" are the individual, smaller documents nested inside a
    broader package (e.g., a specific proposed rule, final rule, or agency notice contained within
    a single daily Federal Register issue). Use this tool when you have a Package ID and need to
    extract or discover the specific rules and articles published inside that issue.

    Args:
        package_id (str): The unique GovInfo identifier for the parent package to extract granules from (e.g., "FR-2023-01-15").
    """
    return await tavily_search_invocation(query=f"Federal Register GovInfo details and granules for package {package_id}",
                                    extra_domains=["govinfo.gov", "federalregister.gov"])