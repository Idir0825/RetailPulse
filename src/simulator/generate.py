#!/usr/bin/env python3
"""Generate deterministic, synthetic *source-system* data for RetailPulse.

This program represents data supplied by a fictional operational company.
It is intentionally NOT the ETL or analytics pipeline the learner will build.
Stdlib only. Re-run with the same seed/parameters for reproducible results.
"""
import argparse
import csv
import json
import random
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

START = datetime(2024, 1, 1, 8, 0)
END = datetime(2026, 9, 30, 20, 0)
CITIES = [
    ("Paris", "Île-de-France"), ("Lyon", "Auvergne-Rhône-Alpes"),
    ("Marseille", "Provence-Alpes-Côte d'Azur"), ("Toulouse", "Occitanie"),
    ("Bordeaux", "Nouvelle-Aquitaine"), ("Lille", "Hauts-de-France"),
    ("Nantes", "Pays de la Loire"), ("Strasbourg", "Grand Est"),
    ("Rennes", "Bretagne"), ("Nice", "Provence-Alpes-Côte d'Azur"),
    ("Grenoble", "Auvergne-Rhône-Alpes"), ("Montpellier", "Occitanie"),
    ("Clermont-Ferrand", "Auvergne-Rhône-Alpes"), ("Dijon", "Bourgogne-Franche-Comté"),
    ("Annecy", "Auvergne-Rhône-Alpes"), ("Rouen", "Normandie"),
    ("Tours", "Centre-Val de Loire"), ("Orléans", "Centre-Val de Loire"),
    ("Metz", "Grand Est"), ("Brest", "Bretagne"),
]
FIRST = ["Camille", "Alex", "Manon", "Hugo", "Lina", "Lucas", "Emma", "Ines", "Jules", "Sarah", "Paul", "Nora", "Adam", "Lea", "Yanis", "Chloe", "Sami", "Zoé"]
LAST = ["Martin", "Bernard", "Dubois", "Petit", "Leroy", "Moreau", "Laurent", "Simon", "Michel", "Garcia", "Roux", "Fontaine", "Thomas", "David", "Lambert", "Lopez", "Faure", "Morel", "Girard"]
CATEGORIES = ["PC portable", "Ecran", "Clavier", "Souris", "Casque", "Smartphone", "Tablette", "Stockage", "Composant PC", "Imprimante", "Camera", "Audio", "Reseau", "Gaming", "Domotique", "Accessoire"]
BRANDS = ["NovaTech", "Hexa", "Electra", "Orion", "Nexus", "Zenit", "Pulse", "Titan", "Axis", "Vertex", "Kairo", "Nebula", "Astra", "Cobalt", "Nimbus", "Vega", "Futura", "Atlas"]
RETURNS = ["Produit defectueux", "Erreur de taille", "Change d'avis", "Commande incorrecte", "Colis endommage", "Produit non conforme"]
CAMPAIGNS = ["WELCOME10", "SOLDES_HIVER", "SOLDES_ETE", "FRENCHDAYS", "BLACKFRIDAY", "CYBERMONDAY", "BACKTOSCHOOL"]


def dt(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


def random_date(rng):
    total_days = (END - START).days
    day = rng.randrange(total_days + 1)
    # modest seasonality: some orders are re-sampled into November and December
    if rng.random() < .16:
        year = rng.choice((2024, 2025))
        day_of_nov = rng.randint(1, 60)
        return datetime(year, 11, 1) + timedelta(days=day_of_nov-1, hours=rng.randint(8, 22), minutes=rng.randint(0,59))
    return START + timedelta(days=day, hours=rng.randint(0, 13), minutes=rng.randint(0, 59))


@contextmanager
def csv_out(root, filename, columns):
    path = root / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as fp:
        w = csv.writer(fp)
        w.writerow(columns)
        yield w


def build(args):
    rng = random.Random(args.seed)
    out = Path(args.output).resolve()
    pg = out / 'seed'
    ext = out / 'external'
    pg.mkdir(parents=True, exist_ok=True)
    ext.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    print(f'Generation RetailPulse (seed={args.seed}) -> {out}', flush=True)

    stores = []
    with csv_out(pg, 'stores.csv', ['store_id', 'store_name', 'city', 'region', 'opened_on']) as w:
        for i in range(1, 53):
            city, region = CITIES[(i-1) % len(CITIES)]
            w.writerow([i, f'RetailPulse {city} {i:02}', city, region, f'{2016+(i%8)}-01-15'])
            stores.append((i,city)); counts['stores'] += 1
    with csv_out(pg, 'warehouses.csv', ['warehouse_id', 'warehouse_name', 'city', 'capacity_units']) as w:
        for i, city in enumerate(['Lyon', 'Paris', 'Lille', 'Bordeaux', 'Marseille', 'Nantes'],1):
            w.writerow([i, f'Hub {city}', city, 80000+i*17000]); counts['warehouses'] += 1

    last_customer_email = None
    with csv_out(pg, 'customers.csv', ['customer_id', 'first_name', 'last_name', 'email', 'city', 'registered_at', 'segment']) as w:
        for i in range(1, args.customers + 1):
            fn, ln = rng.choice(FIRST), rng.choice(LAST)
            city, _ = rng.choice(CITIES)
            email = f'{fn.lower()}.{ln.lower()}.{i}@example.test'
            if i > 4 and i % 331 == 0:
                email = last_customer_email  # duplicate email from the previous customer
            if i % 181 == 0:
                email = ''  # deliberate missing source value
            reg = datetime(2022,1,1) + timedelta(days=rng.randrange(730))
            w.writerow([i, fn,ln,email,city,dt(reg),rng.choices(['standard','premium','pro'],[72,23,5])[0]])
            last_customer_email = email
            counts['customers'] += 1

    product_prices = {}
    with csv_out(pg, 'products.csv', ['product_id','sku','category','brand','product_name','list_price_eur','cost_eur','launched_on','is_active']) as w:
        for i in range(1, args.products+1):
            cat, brand = rng.choice(CATEGORIES), rng.choice(BRANDS)
            price = round(rng.uniform(8,140) if cat in {'Souris','Clavier','Accessoire','Stockage'} else rng.uniform(65,1800),2)
            price = round(price + .99 - price%1,2)
            cost = round(price * rng.uniform(.49,.81),2)
            product_prices[i] = price
            w.writerow([i,f'SKU-{i:06d}',cat,brand,f'{brand} {cat} Series {i%119:03}',f'{price:.2f}',f'{cost:.2f}',f'{2022+i%3}-02-01', 'true' if i%17 else 'false'])
            counts['products']+=1

    # Enforce all FK relations in transactional source; inject dirty records only in external feeds.
    order_dates = {}
    successful_orders = []  # (order_id, first_product_id, date, location_type, location_id)
    order_ids = []
    order_item_id = 0
    payment_id = 0
    shipment_id = 0
    return_id = 0
    statuses = Counter()
    order_ch = Counter()
    with csv_out(pg,'orders.csv',['order_id','customer_id','store_id','warehouse_id','channel','ordered_at','updated_at','status','shipping_fee_eur','promo_code','total_amount_eur','currency']) as orders, \
         csv_out(pg,'order_items.csv',['order_item_id','order_id','product_id','quantity','unit_price_eur','discount_amount_eur','line_total_eur']) as items, \
         csv_out(pg,'payments.csv',['payment_id','order_id','payment_at','method','status','amount_eur','provider_reference']) as payments, \
         csv_out(pg,'shipments.csv',['shipment_id','order_id','warehouse_id','carrier','shipped_at','promised_at','delivered_at','status']) as shipments, \
         csv_out(pg,'returns.csv',['return_id','order_id','returned_at','reason','refund_amount_eur','status']) as returns:
        for i in range(1,args.orders+1):
            d = random_date(rng)
            age=(END-d).days
            channel = rng.choices(['web','mobile','store'],[51,32,17])[0]
            store = rng.randint(1,52) if channel=='store' else ''
            warehouse = rng.randint(1,6) if channel!='store' else ''
            customer = rng.randint(1,args.customers)
            if age<14:
                status=rng.choices(['delivered','shipped','processing','cancelled','returned'],[42,25,22,8,3])[0]
            else:
                status=rng.choices(['delivered','cancelled','returned'],[86,8,6])[0]
            promo = rng.choice(CAMPAIGNS) if rng.random()<.11 else ''
            subtotal=0.0
            n_items=rng.choices([1,2,3,4,5],[25,35,24,12,4])[0]
            first_product = None
            for _ in range(n_items):
                order_item_id+=1
                product_id=rng.randint(1,args.products)
                if first_product is None: first_product = product_id
                unit=product_prices[product_id]
                qty=rng.choices([1,2,3],[84,13,3])[0]
                disc=round(unit*qty*rng.uniform(.05,.24),2) if promo else 0
                line=round(unit*qty-disc,2)
                subtotal=round(subtotal+line,2)
                items.writerow([order_item_id,i,product_id,qty,f'{unit:.2f}',f'{disc:.2f}',f'{line:.2f}'])
            shipping_fee=round(rng.choice([0,0,0,4.99,7.99,12.99]),2) if channel!='store' else 0.0
            total=round(subtotal+shipping_fee,2)
            update=d+timedelta(days=rng.randint(0,min(9,max(0,age))))
            if update>END: update=END
            orders.writerow([i,customer,store,warehouse,channel,dt(d),dt(update),status,f'{shipping_fee:.2f}',promo,f'{total:.2f}','EUR'])
            order_dates[i]=d
            order_ids.append(i)
            statuses[status]+=1;order_ch[channel]+=1;counts['orders']+=1
            # A failed payment attempt can precede a successful one.
            method=rng.choices(['card','paypal','bank_transfer','gift_card'],[79,13,5,3])[0]
            if status not in ('cancelled','processing') and rng.random()<.055:
                payment_id+=1
                payments.writerow([payment_id,i,dt(d),'card','failed',f'{total:.2f}',f'RP-{payment_id:09}']);counts['payments']+=1
            payment_id+=1
            paystatus='failed' if status=='cancelled' else 'pending' if status=='processing' else 'succeeded'
            payments.writerow([payment_id,i,dt(d),method,paystatus,f'{total:.2f}',f'RP-{payment_id:09}']);counts['payments']+=1
            if status in ('delivered','returned','shipped'):
                shipment_id+=1
                shipped=d+timedelta(hours=rng.randint(8,65))
                promised=d+timedelta(days=rng.randint(3,6))
                delivered=shipped+timedelta(days=rng.randint(1,9))
                shipment_status='in_transit' if status=='shipped' else 'delivered'
                shipments.writerow([shipment_id,i,warehouse or rng.randint(1,6),rng.choice(['Colissimo','Chronopost','DHL','Mondial Relay']),dt(shipped),dt(promised),'' if status=='shipped' else dt(delivered),shipment_status])
                counts['shipments']+=1
                if status=='returned' or (status=='delivered' and rng.random()<.012):
                    return_id+=1
                    refund=round(total*rng.uniform(.45,1.0),2)
                    returns.writerow([return_id,i,dt(delivered+timedelta(days=rng.randint(1,18))),rng.choice(RETURNS),f'{refund:.2f}',rng.choices(['accepted','requested','rejected'],[88,9,3])[0]])
                    counts['returns']+=1
            if status not in ('cancelled','processing'):
                successful_orders.append((i, first_product, d, 'store' if channel == 'store' else 'warehouse', store or warehouse))
            if i%50000==0: print(f'  {i:,} commandes produites', flush=True)
    counts['order_items']=order_item_id

    with csv_out(pg,'inventory_movements.csv',['movement_id','product_id','location_type','location_id','event_at','delta_qty','reason','order_id']) as w:
        reasons=['replenishment','sale','return','adjustment','damage']
        weights=[24,62,7,5,2]
        for i in range(1,args.inventory_movements+1):
            reason=rng.choices(reasons,weights)[0]
            kind=rng.choices(['store','warehouse'],[56,44])[0]
            location=rng.randint(1,52) if kind=='store' else rng.randint(1,6)
            delta=rng.randint(3,100) if reason=='replenishment' else rng.randint(1,3) if reason=='return' else -rng.randint(1,5)
            order_ref=''
            product_id=rng.randint(1,args.products)
            event_time=random_date(rng)
            if reason=='sale':
                order_ref, product_id, event_time, kind, location = rng.choice(successful_orders)
            w.writerow([i,product_id,kind,location,dt(event_time),delta,reason,order_ref]);counts['inventory_movements']+=1

    with csv_out(pg,'support_tickets.csv',['ticket_id','order_id','opened_at','channel','topic','priority','status']) as w:
        for i in range(1,args.support_tickets+1):
            orderid=rng.choice(order_ids)
            opened=order_dates[orderid]+timedelta(days=rng.randint(0,16))
            w.writerow([i,orderid,dt(opened),rng.choice(['email','chat','phone']),rng.choice(['delivery','refund','payment','product','account']),rng.choices(['low','medium','high'],[40,45,15])[0],rng.choice(['open','pending','resolved'])]);counts['support_tickets']+=1

    with csv_out(ext,'supplier_prices.csv',['event_id','supplier_id','sku','effective_at','new_cost_eur','currency']) as w:
        for i in range(1,args.supplier_events+1):
            price=round(rng.uniform(2,1200),2)
            if i%151==0: value='N/A' # deliberately bad string
            elif i%271==0: value='-12.00' # suspicious negative cost
            else: value=f'{price:.2f}'
            eventid=i-1 if i%193==0 else i # deliberately repeated source identifiers
            currency='???' if i%401==0 else 'EUR'
            w.writerow([eventid,rng.randint(1,140),f'SKU-{rng.randint(1,args.products):06}',dt(random_date(rng)),value,currency]);counts['supplier_prices']+=1

    # Raw website events: semi-structured JSON, duplicate IDs, null identities, out-of-order arrival.
    with (ext/'web_events.jsonl').open('w',encoding='utf-8') as fp:
        for i in range(1,args.web_events+1):
            eventid=i-1 if i%211==0 else i
            who = None if rng.random()<.30 else rng.randint(1,args.customers)
            event_time=random_date(rng)
            ingestion_delay = timedelta(minutes=rng.randint(1,240)) if i%73 else timedelta(days=rng.randint(2,20))
            event={'event_id':f'evt-{eventid}', 'event_time':dt(event_time),
                   'ingested_at':dt(event_time + ingestion_delay),
                   'anonymous_id':f'session-{rng.randint(1,35000)}',
                   'customer_id':who, 'event_type':rng.choices(['page_view','search','product_view','add_to_cart','checkout'],[43,14,26,12,5])[0],
                   'product_id':rng.randint(1,args.products), 'device':rng.choice(['desktop','mobile','tablet']),
                   'source':rng.choice(['organic','ads','email','direct','social'])}
            if i%317==0: event['custom_payload']={'experiment':'checkout_v2','variant':'B'}
            fp.write(json.dumps(event,ensure_ascii=False,separators=(',',':'))+'\n')
            counts['web_events']+=1
            if i%200000==0:print(f'  {i:,} evenements web produits',flush=True)

    manifest={'project':'RetailPulse','synthetic':True,'seed':args.seed,
              'date_range':['2024-01-01','2026-09-30'],
              'counts':dict(counts),'order_status_distribution':dict(statuses),
              'order_channel_distribution':dict(order_ch),
              'purpose':'Simulated upstream sources; not a warehouse or transformed dataset.',
              'quality_cases':['missing and duplicate customer emails','multiple payment attempts','cancellations','late shipments','returns','duplicate web event IDs','invalid supplier prices','duplicated supplier event IDs','unexpected supplier currency','nullable event identities']}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('OK: '+json.dumps(dict(counts),ensure_ascii=False),flush=True)


def main():
    p=argparse.ArgumentParser(description='Generate synthetic RetailPulse upstream data (stdlib only)')
    p.add_argument('--output',default='data',help='Directory containing seed/ and external/')
    p.add_argument('--seed',type=int,default=20261010)
    p.add_argument('--customers',type=int,default=12500)
    p.add_argument('--products',type=int,default=2500)
    p.add_argument('--orders',type=int,default=200000)
    p.add_argument('--web-events',type=int,default=400000)
    p.add_argument('--inventory-movements',type=int,default=250000)
    p.add_argument('--support-tickets',type=int,default=9000)
    p.add_argument('--supplier-events',type=int,default=18000)
    a=p.parse_args()
    for name in ('customers','products','orders','web_events','inventory_movements','support_tickets','supplier_events'):
        if getattr(a,name)<1: p.error(name+' must be positive')
    build(a)

if __name__=='__main__':
    main()
