# erp-mcp

MCP server ket noi Claude Code voi ERPNext/Frappe (platform.nguoithuanviet.com) qua REST API,
dung xac thuc API Key/API Secret.

## Cai dat

```bash
pip install -e .
```

## Cau hinh

1. Sao chep `.env.example` thanh `.env`.
2. Dien `FRAPPE_URL`, `FRAPPE_API_KEY`, `FRAPPE_API_SECRET` (lay tu Nguoi dung > Truy cap API trong Frappe).
3. **Khong commit file `.env`** — file nay da co trong `.gitignore`.

> Luu y bao mat: neu API Key/Secret tung bi lo (vi du chup man hinh, dan vao chat...),
> hay vao Frappe > Nguoi dung > Truy cap API > thu hoi khoa cu va tao khoa moi, roi cap
> nhat lai `.env`.

## Chay thu server

```bash
python -m erp_mcp.server
```

## Dang ky voi Claude Code

File `.mcp.json` o goc repo da khai bao server ten `erp`. Mo repo nay bang Claude Code,
server se tu duoc phat hien (co the can `claude mcp list` / khoi dong lai session de nap).

## Cac tool MCP co san

- `erp_list_docs(doctype, filters, fields, limit_page_length, order_by)` — liet ke ban ghi
- `erp_get_doc(doctype, name)` — lay chi tiet 1 ban ghi
- `erp_create_doc(doctype, data)` — tao moi ban ghi (data la chuoi JSON)
- `erp_update_doc(doctype, name, data)` — cap nhat ban ghi
- `erp_delete_doc(doctype, name)` — xoa ban ghi
- `erp_call_method(method_path, params)` — goi mot whitelisted method tuy chinh cua Frappe

`filters`/`fields`/`params`/`data` la cac tham so dang chuoi JSON, vi du:

```
erp_list_docs(doctype="ToDo", filters='[["status","=","Open"]]', fields='["name","description"]')
```

## Xu ly loi ket noi

Neu chay trong moi truong Claude Code on the web (sandbox), truy cap mang ra ngoai
bi gioi han theo chinh sach cua environment — mien khong nam trong danh sach cho phep
se bi tu choi (403 tu proxy, khong phai loi tu Frappe). Neu gap loi nay, hay:

- Chay server tren may local (khong bi gioi han mang), hoac
- Cau hinh lai network policy cua environment de cho phep domain ERPNext cua ban.

