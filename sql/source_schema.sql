-- RetailPulse operational system: input data (not your target warehouse).
CREATE SCHEMA IF NOT EXISTS source;
CREATE TABLE IF NOT EXISTS source.stores (
  store_id INTEGER PRIMARY KEY, store_name TEXT NOT NULL, city TEXT NOT NULL,
  region TEXT NOT NULL, opened_on DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS source.warehouses (
  warehouse_id INTEGER PRIMARY KEY, warehouse_name TEXT NOT NULL,
  city TEXT NOT NULL, capacity_units INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS source.customers (
  customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
  email TEXT, city TEXT NOT NULL, registered_at TIMESTAMP NOT NULL, segment TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source.products (
  product_id INTEGER PRIMARY KEY, sku TEXT NOT NULL UNIQUE, category TEXT NOT NULL,
  brand TEXT NOT NULL, product_name TEXT NOT NULL,
  list_price_eur NUMERIC(12,2) NOT NULL, cost_eur NUMERIC(12,2) NOT NULL,
  launched_on DATE NOT NULL, is_active BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS source.orders (
  order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES source.customers(customer_id),
  store_id INTEGER REFERENCES source.stores(store_id),
  warehouse_id INTEGER REFERENCES source.warehouses(warehouse_id),
  channel TEXT NOT NULL, ordered_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL,
  status TEXT NOT NULL, shipping_fee_eur NUMERIC(12,2) NOT NULL,
  promo_code TEXT, total_amount_eur NUMERIC(14,2) NOT NULL,
  currency CHAR(3) NOT NULL
);
CREATE TABLE IF NOT EXISTS source.order_items (
  order_item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES source.orders(order_id),
  product_id INTEGER NOT NULL REFERENCES source.products(product_id),
  quantity INTEGER NOT NULL, unit_price_eur NUMERIC(12,2) NOT NULL,
  discount_amount_eur NUMERIC(12,2) NOT NULL, line_total_eur NUMERIC(14,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS source.payments (
  payment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES source.orders(order_id),
  payment_at TIMESTAMP NOT NULL, method TEXT NOT NULL, status TEXT NOT NULL,
  amount_eur NUMERIC(14,2) NOT NULL, provider_reference TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS source.shipments (
  shipment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES source.orders(order_id),
  warehouse_id INTEGER NOT NULL REFERENCES source.warehouses(warehouse_id),
  carrier TEXT NOT NULL, shipped_at TIMESTAMP NOT NULL, promised_at TIMESTAMP NOT NULL,
  delivered_at TIMESTAMP, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source.returns (
  return_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES source.orders(order_id),
  returned_at TIMESTAMP NOT NULL, reason TEXT NOT NULL,
  refund_amount_eur NUMERIC(14,2) NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source.inventory_movements (
  movement_id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL REFERENCES source.products(product_id),
  location_type TEXT NOT NULL, location_id INTEGER NOT NULL,
  event_at TIMESTAMP NOT NULL, delta_qty INTEGER NOT NULL,
  reason TEXT NOT NULL, order_id INTEGER REFERENCES source.orders(order_id)
);
CREATE TABLE IF NOT EXISTS source.support_tickets (
  ticket_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES source.orders(order_id),
  opened_at TIMESTAMP NOT NULL, channel TEXT NOT NULL, topic TEXT NOT NULL,
  priority TEXT NOT NULL, status TEXT NOT NULL
);
