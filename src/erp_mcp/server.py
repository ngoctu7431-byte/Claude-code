import json
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

from erp_mcp.frappe_client import FrappeClient

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

mcp = MCPServer("erp-mcp")

_client: FrappeClient | None = None


def get_client() -> FrappeClient:
    global _client
    if _client is None:
        _client = FrappeClient()
    return _client


@mcp.tool()
def erp_list_docs(
    doctype: str,
    filters: str = "",
    fields: str = "",
    limit_page_length: int = 20,
    order_by: str = "",
) -> str:
    """Liet ke ban ghi cua mot doctype trong ERPNext/Frappe.

    filters: chuoi JSON kieu Frappe, vi du '[["status","=","Open"]]'
    fields: chuoi JSON danh sach truong, vi du '["name","status"]'
    """
    parsed_filters = json.loads(filters) if filters else None
    parsed_fields = json.loads(fields) if fields else None
    docs = get_client().list_docs(
        doctype,
        filters=parsed_filters,
        fields=parsed_fields,
        limit_page_length=limit_page_length,
        order_by=order_by or None,
    )
    return json.dumps(docs, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_get_doc(doctype: str, name: str) -> str:
    """Lay chi tiet mot ban ghi theo doctype va ten (ID)."""
    doc = get_client().get_doc(doctype, name)
    return json.dumps(doc, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_create_doc(doctype: str, data: str) -> str:
    """Tao moi mot ban ghi. data la chuoi JSON chua cac truong cua doctype."""
    doc = get_client().create_doc(doctype, json.loads(data))
    return json.dumps(doc, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_update_doc(doctype: str, name: str, data: str) -> str:
    """Cap nhat mot ban ghi. data la chuoi JSON chua cac truong can sua."""
    doc = get_client().update_doc(doctype, name, json.loads(data))
    return json.dumps(doc, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_delete_doc(doctype: str, name: str) -> str:
    """Xoa mot ban ghi theo doctype va ten (ID)."""
    get_client().delete_doc(doctype, name)
    return f"Da xoa {doctype}/{name}"


@mcp.tool()
def erp_list_orders(
    status: str = "",
    customer: str = "",
    from_date: str = "",
    to_date: str = "",
    limit_page_length: int = 20,
) -> str:
    """Liet ke Sales Order (don hang) voi cac bo loc thuong dung.

    status: vi du 'Draft', 'To Deliver and Bill', 'Completed', 'Cancelled'
    from_date/to_date: dang 'YYYY-MM-DD', loc theo transaction_date
    """
    filters: list = []
    if status:
        filters.append(["status", "=", status])
    if customer:
        filters.append(["customer", "=", customer])
    if from_date:
        filters.append(["transaction_date", ">=", from_date])
    if to_date:
        filters.append(["transaction_date", "<=", to_date])

    docs = get_client().list_docs(
        "Sales Order",
        filters=filters or None,
        fields=["name", "customer", "status", "transaction_date", "grand_total", "currency"],
        limit_page_length=limit_page_length,
        order_by="transaction_date desc",
    )
    return json.dumps(docs, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_sync_orders(modified_since: str = "", status: str = "", limit_page_length: int = 100) -> str:
    """Dong bo Sales Order day du (gom bang con items) tu ERPNext.

    modified_since: chuoi 'YYYY-MM-DD HH:MM:SS', chi lay ban ghi cap nhat tu thoi diem nay.
    Bo trong se lay theo limit_page_length ban ghi moi cap nhat gan day nhat.
    """
    orders = get_client().sync_orders(
        modified_since=modified_since or None,
        status=status or None,
        limit_page_length=limit_page_length,
    )
    return json.dumps(orders, ensure_ascii=False, indent=2)


@mcp.tool()
def erp_call_method(method_path: str, params: str = "") -> str:
    """Goi mot whitelisted method tuy chinh tren Frappe, vi du 'frappe.client.get_count'.

    params: chuoi JSON chua tham so cho method.
    """
    parsed_params = json.loads(params) if params else None
    result = get_client().call_method(method_path, parsed_params)
    return json.dumps(result, ensure_ascii=False, indent=2)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
