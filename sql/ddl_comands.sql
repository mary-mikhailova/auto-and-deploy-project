CREATE TABLE public.sales_shop_cash (
	id serial4 NOT NULL,
	dt timestamp NULL,
	shop_num int4 NULL,
	cash_num int4 NULL,
	doc_id varchar NULL,
	item varchar NULL,
	category varchar NULL,
	amount int4 NULL,
	price numeric NULL,
	discount numeric NULL,
	CONSTRAINT sales_shop_cash_pk PRIMARY KEY (id),
	CONSTRAINT sales_shop_cash_unique UNIQUE (dt, doc_id)
);