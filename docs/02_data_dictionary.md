# RetailPulse — Upstream data dictionary

All records are **synthetic**. Main date range: January 2024 through September 2026.

## PostgreSQL `source` schema

| Table | Grain | Main keys | Purpose |
|---|---|---|---|
| `stores` | One retail store | `store_id` | Name, city, region and opening date |
| `warehouses` | One warehouse | `warehouse_id` | Location and capacity |
| `customers` | One customer | `customer_id` | Synthetic identity, email, city and segment |
| `products` | One sellable SKU | `product_id`, `sku` | Category, brand, list price, cost and activation |
| `orders` | One order | `order_id`, `customer_id` | Channel, status, store/warehouse allocation, timestamps and total |
| `order_items` | One order line | `order_item_id`, `order_id`, `product_id` | Quantity, sale-time prices, discounts and totals |
| `payments` | One payment attempt | `payment_id`, `order_id` | Status, method, attempt amount and provider reference |
| `shipments` | One shipment | `shipment_id`, `order_id` | Carrier, planned/actual delivery and status |
| `returns` | One return request | `return_id`, `order_id` | Return reason, amount to refund, status |
| `inventory_movements` | One inventory movement | `movement_id`, `product_id` | Location, quantity delta, timestamp and reason |
| `support_tickets` | One support ticket | `ticket_id`, `order_id` | Topic, priority, status |

**Important semantics:** `source.orders.total_amount_eur` is an order amount, not necessarily collected revenue. Multiple payment attempts may exist per order, and `returned` does not imply a full refund. These definitions need explicit business rules before financial reporting is introduced.

**Channel allocation in the generated source:** store orders are normally associated with `store_id`; web/mobile orders with `warehouse_id`. The nullable column on the other fulfillment path can be intentional. See TICKET-002 for the baseline rule checks.

## File sources

- **`data/external/supplier_prices.csv`** — a supplier purchase-price event per row: `event_id`, `supplier_id`, `sku`, `effective_at`, `new_cost_eur`, `currency`. Some values are malformed, negative, duplicate or expressed in unexpected currencies.
- **`data/external/web_events.jsonl`** — one browsing event per JSON line (e.g., product view, search, checkout). Event identifiers may repeat; customer identities may be missing; the semi-structured payload may evolve.

## Synthetic quality scenarios

- Missing or duplicated customer emails.
- Multiple payment attempts, rejected/pending payments, cancellation and returns.
- Late shipments and various discounts or channels.
- Repeated supplier/web event identifiers and malformed supplier prices.
- Anonymous website activity and optional event fields.

This generator creates plausible but synthetic distributions; it does not model a specific real retailer's financial performance.

See [`../data/manifest.json`](../data/manifest.json) for the precise seeded counts and [`../sql/source_schema.sql`](../sql/source_schema.sql) for data types and foreign keys.
