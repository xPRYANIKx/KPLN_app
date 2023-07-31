PGDMP          9                {            kpln_db    15.3    15.3 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    kpln_db    DATABASE     {   CREATE DATABASE kpln_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE kpln_db;
                postgres    false            �           0    0    SCHEMA public    ACL     )   GRANT ALL ON SCHEMA public TO kpln_user;
                   pg_database_owner    false    5            �            1259    16399    contract_purposes    TABLE     }   CREATE TABLE public.contract_purposes (
    contract_purpose_id integer NOT NULL,
    contract_purpose_name text NOT NULL
);
 %   DROP TABLE public.contract_purposes;
       public         heap    postgres    false            �           0    0    TABLE contract_purposes    COMMENT     |   COMMENT ON TABLE public.contract_purposes IS 'Назначения (Учитывается / Не учитывается)';
          public          postgres    false    214            �           0    0    TABLE contract_purposes    ACL     :   GRANT ALL ON TABLE public.contract_purposes TO kpln_user;
          public          postgres    false    214            �            1259    16404 (   contract_purposes_contract_purpos_id_seq    SEQUENCE     �   ALTER TABLE public.contract_purposes ALTER COLUMN contract_purpose_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_purposes_contract_purpos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    214            �           0    0 1   SEQUENCE contract_purposes_contract_purpos_id_seq    ACL     T   GRANT ALL ON SEQUENCE public.contract_purposes_contract_purpos_id_seq TO kpln_user;
          public          postgres    false    215            �            1259    16405    contract_statuses    TABLE     {   CREATE TABLE public.contract_statuses (
    contract_status_id integer NOT NULL,
    contract_status_name text NOT NULL
);
 %   DROP TABLE public.contract_statuses;
       public         heap    postgres    false            �           0    0    TABLE contract_statuses    ACL     :   GRANT ALL ON TABLE public.contract_statuses TO kpln_user;
          public          postgres    false    216            �            1259    16410 (   contract_statuses_contract_status_id_seq    SEQUENCE     �   ALTER TABLE public.contract_statuses ALTER COLUMN contract_status_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_statuses_contract_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �           0    0 1   SEQUENCE contract_statuses_contract_status_id_seq    ACL     T   GRANT ALL ON SEQUENCE public.contract_statuses_contract_status_id_seq TO kpln_user;
          public          postgres    false    217            �            1259    16411    contract_types    TABLE     t   CREATE TABLE public.contract_types (
    contract_type_id integer NOT NULL,
    contract_type_name text NOT NULL
);
 "   DROP TABLE public.contract_types;
       public         heap    postgres    false            �           0    0    TABLE contract_types    ACL     7   GRANT ALL ON TABLE public.contract_types TO kpln_user;
          public          postgres    false    218            �            1259    16416 #   contract_types_contract_type_id_seq    SEQUENCE     �   ALTER TABLE public.contract_types ALTER COLUMN contract_type_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_types_contract_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    218            �           0    0 ,   SEQUENCE contract_types_contract_type_id_seq    ACL     O   GRANT ALL ON SEQUENCE public.contract_types_contract_type_id_seq TO kpln_user;
          public          postgres    false    219            �            1259    16417    our_companies    TABLE     �   CREATE TABLE public.our_companies (
    contractor_id integer NOT NULL,
    contractor_name text NOT NULL,
    vat boolean NOT NULL,
    contractor_value real GENERATED ALWAYS AS (
CASE
    WHEN vat THEN 1.2
    ELSE (1)::numeric
END) STORED NOT NULL
);
 !   DROP TABLE public.our_companies;
       public         heap    postgres    false            �           0    0    TABLE our_companies    COMMENT     U   COMMENT ON TABLE public.our_companies IS 'Список наших компаний';
          public          postgres    false    220            �           0    0    TABLE our_companies    ACL     6   GRANT ALL ON TABLE public.our_companies TO kpln_user;
          public          postgres    false    220            �            1259    16423    contractors_contractor_id_seq    SEQUENCE     �   ALTER TABLE public.our_companies ALTER COLUMN contractor_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contractors_contractor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    220            �           0    0 &   SEQUENCE contractors_contractor_id_seq    ACL     I   GRANT ALL ON SEQUENCE public.contractors_contractor_id_seq TO kpln_user;
          public          postgres    false    221            �            1259    16424 	   contracts    TABLE     q  CREATE TABLE public.contracts (
    contract_id integer NOT NULL,
    contract_name character varying(100) NOT NULL,
    stage character varying(100),
    department character varying(20),
    contract_number character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    start_date date NOT NULL,
    costs numeric
);
    DROP TABLE public.contracts;
       public         heap    postgres    false            �           0    0    TABLE contracts    ACL     2   GRANT ALL ON TABLE public.contracts TO kpln_user;
          public          postgres    false    222            �            1259    16430    contracts_contracts_id_seq    SEQUENCE     �   ALTER TABLE public.contracts ALTER COLUMN contract_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contracts_contracts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    222            �           0    0 #   SEQUENCE contracts_contracts_id_seq    ACL     F   GRANT ALL ON SEQUENCE public.contracts_contracts_id_seq TO kpln_user;
          public          postgres    false    223            �            1259    16431    new_objects    TABLE     �  CREATE TABLE public.new_objects (
    object_id integer NOT NULL,
    object_name text NOT NULL,
    contract_type text NOT NULL,
    date_row date NOT NULL,
    contract_number text NOT NULL,
    customer text NOT NULL,
    contractor text NOT NULL,
    contract_comment text,
    contract_status text NOT NULL,
    contract_purpose text NOT NULL,
    vat text NOT NULL,
    vat_value real NOT NULL
);
    DROP TABLE public.new_objects;
       public         heap    postgres    false            �           0    0    TABLE new_objects    ACL     4   GRANT ALL ON TABLE public.new_objects TO kpln_user;
          public          postgres    false    224            �            1259    16436    new_objects_object_id_seq    SEQUENCE     �   CREATE SEQUENCE public.new_objects_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.new_objects_object_id_seq;
       public          postgres    false    224            �           0    0    new_objects_object_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.new_objects_object_id_seq OWNED BY public.new_objects.object_id;
          public          postgres    false    225            �           0    0 "   SEQUENCE new_objects_object_id_seq    ACL     E   GRANT ALL ON SEQUENCE public.new_objects_object_id_seq TO kpln_user;
          public          postgres    false    225            �            1259    16437    new_objects_object_id_seq1    SEQUENCE     �   ALTER TABLE public.new_objects ALTER COLUMN object_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.new_objects_object_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    224            �           0    0 #   SEQUENCE new_objects_object_id_seq1    ACL     F   GRANT ALL ON SEQUENCE public.new_objects_object_id_seq1 TO kpln_user;
          public          postgres    false    226            �            1259    16438    objects    TABLE     l   CREATE TABLE public.objects (
    object_id integer NOT NULL,
    object_name character varying NOT NULL
);
    DROP TABLE public.objects;
       public         heap    postgres    false            �           0    0    TABLE objects    ACL     0   GRANT ALL ON TABLE public.objects TO kpln_user;
          public          postgres    false    227            �            1259    16443    objects_object_id_seq    SEQUENCE     �   ALTER TABLE public.objects ALTER COLUMN object_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.objects_object_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    227            �           0    0    SEQUENCE objects_object_id_seq    ACL     A   GRANT ALL ON SEQUENCE public.objects_object_id_seq TO kpln_user;
          public          postgres    false    228            �            1259    32872    payment_agreed_statuses    TABLE     �   CREATE TABLE public.payment_agreed_statuses (
    payment_agreed_status_id smallint NOT NULL,
    payment_agreed_status_name text NOT NULL,
    payment_agreed_status_category text NOT NULL
);
 +   DROP TABLE public.payment_agreed_statuses;
       public         heap    postgres    false            �           0    0    TABLE payment_agreed_statuses    COMMENT     �  COMMENT ON TABLE public.payment_agreed_statuses IS 'Статусы платежей. Различаются категориями:
Статусы Андрея - статусы согласования - "Черновик / "Реком." / "Аннулирован" / "К рассмотрению"
Статусы оплаты - "В оплате" / "Полная оплата" / "Частичная оплата"';
          public          postgres    false    237            �            1259    32950    payment_cost_items    TABLE     �   CREATE TABLE public.payment_cost_items (
    cost_item_id smallint NOT NULL,
    cost_item_name text NOT NULL,
    cost_item_category text NOT NULL
);
 &   DROP TABLE public.payment_cost_items;
       public         heap    postgres    false            �           0    0    TABLE payment_cost_items    COMMENT     a   COMMENT ON TABLE public.payment_cost_items IS 'СТАТЬЯ ЗАТРАТ (ТИП ЗАЯВКИ)';
          public          postgres    false    242            �            1259    32953 #   payment_cost_items_cost_item_id_seq    SEQUENCE     �   ALTER TABLE public.payment_cost_items ALTER COLUMN cost_item_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payment_cost_items_cost_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    242            �            1259    32922    payments_approval    TABLE       CREATE TABLE public.payments_approval (
    payment_approval_id integer NOT NULL,
    payment_id integer NOT NULL,
    payment_approval_status_id smallint NOT NULL,
    payment_approval_date time with time zone NOT NULL,
    payment_approval_sum numeric(9,2) NOT NULL
);
 %   DROP TABLE public.payments_approval;
       public         heap    postgres    false            �           0    0    TABLE payments_approval    COMMENT     �   COMMENT ON TABLE public.payments_approval IS 'Таблица согласованных платежей
Отображаются все когда-либо согласованные платежи';
          public          postgres    false    239            �            1259    32921 %   payments_agreed_payment_agreed_id_seq    SEQUENCE     �   ALTER TABLE public.payments_approval ALTER COLUMN payment_approval_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_agreed_payment_agreed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    239            �            1259    33001    payments_andrew_statuses    TABLE       CREATE TABLE public.payments_andrew_statuses (
    payment_andrew_status_id smallint NOT NULL,
    payment_id smallint NOT NULL,
    status_id smallint NOT NULL,
    user_id smallint NOT NULL,
    create_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
 ,   DROP TABLE public.payments_andrew_statuses;
       public         heap    postgres    false            �           0    0    TABLE payments_andrew_statuses    COMMENT     w   COMMENT ON TABLE public.payments_andrew_statuses IS 'Статусы обобрения платеже Андреем';
          public          postgres    false    244            �           0    0 8   COLUMN payments_andrew_statuses.payment_andrew_status_id    COMMENT     a   COMMENT ON COLUMN public.payments_andrew_statuses.payment_andrew_status_id IS 'id записи';
          public          postgres    false    244            �           0    0 *   COLUMN payments_andrew_statuses.payment_id    COMMENT     S   COMMENT ON COLUMN public.payments_andrew_statuses.payment_id IS 'id заявки';
          public          postgres    false    244            �           0    0 )   COLUMN payments_andrew_statuses.status_id    COMMENT     �   COMMENT ON COLUMN public.payments_andrew_statuses.status_id IS 'id статуса заявки (черновки, аннул и тд)';
          public          postgres    false    244            �            1259    33022 5   payments_andrew_statuses_payment_andrew_status_id_seq    SEQUENCE       ALTER TABLE public.payments_andrew_statuses ALTER COLUMN payment_andrew_status_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_andrew_statuses_payment_andrew_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    244            �            1259    32942    payments_paid    TABLE     �   CREATE TABLE public.payments_paid (
    payment_pay_id integer NOT NULL,
    payment_id integer NOT NULL,
    payment_paid_status_id smallint,
    payment_full_paid_status boolean DEFAULT false NOT NULL,
    payment_paid_sum numeric(9,2) NOT NULL
);
 !   DROP TABLE public.payments_paid;
       public         heap    postgres    false            �           0    0    TABLE payments_paid    COMMENT     a   COMMENT ON TABLE public.payments_paid IS 'Таблица оплаченных платежей';
          public          postgres    false    241            �           0    0 +   COLUMN payments_paid.payment_paid_status_id    COMMENT     �   COMMENT ON COLUMN public.payments_paid.payment_paid_status_id IS 'ЗАКРЫТЬ ТОЛЬКО ПОСЛЕ ПОЛНОЙ ОПЛАТЫ';
          public          postgres    false    241            �            1259    32941     payments_paid_payment_pay_id_seq    SEQUENCE     �   ALTER TABLE public.payments_paid ALTER COLUMN payment_pay_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_paid_payment_pay_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    241            �            1259    32864    payments_summary_tab    TABLE     }  CREATE TABLE public.payments_summary_tab (
    payment_id integer NOT NULL,
    our_companies_id smallint NOT NULL,
    cost_item_id smallint NOT NULL,
    payment_number text NOT NULL,
    basis_of_payment text NOT NULL,
    payment_description text NOT NULL,
    object_id smallint,
    partner text,
    payment_sum numeric(11,2) NOT NULL,
    payment_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    payment_due_date date NOT NULL,
    payment_full_agreed_status boolean DEFAULT false NOT NULL,
    payment_owner smallint,
    responsible smallint NOT NULL,
    payment_status text DEFAULT 'new'::text NOT NULL
);
 (   DROP TABLE public.payments_summary_tab;
       public         heap    postgres    false            �           0    0    TABLE payments_summary_tab    COMMENT     b   COMMENT ON TABLE public.payments_summary_tab IS 'Сводная таблица платежей';
          public          postgres    false    236            �           0    0 &   COLUMN payments_summary_tab.payment_id    COMMENT     Q   COMMENT ON COLUMN public.payments_summary_tab.payment_id IS '--id заявки';
          public          postgres    false    236            �           0    0 ,   COLUMN payments_summary_tab.our_companies_id    COMMENT     U   COMMENT ON COLUMN public.payments_summary_tab.our_companies_id IS 'СИП/КПЛН';
          public          postgres    false    236            �           0    0 (   COLUMN payments_summary_tab.cost_item_id    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.cost_item_id IS 'СТАТЬЯ ЗАТРАТ';
          public          postgres    false    236            �           0    0 *   COLUMN payments_summary_tab.payment_number    COMMENT     V   COMMENT ON COLUMN public.payments_summary_tab.payment_number IS '№ ПЛАТЕЖА';
          public          postgres    false    236            �           0    0 ,   COLUMN payments_summary_tab.basis_of_payment    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.basis_of_payment IS 'ОСНОВАНИЕ ПЛАТЕЖА, № ДОГОВОРА/ № СЧЁТА';
          public          postgres    false    236            �           0    0 /   COLUMN payments_summary_tab.payment_description    COMMENT     Y   COMMENT ON COLUMN public.payments_summary_tab.payment_description IS 'ОПИСАНИЕ';
          public          postgres    false    236            �           0    0 %   COLUMN payments_summary_tab.object_id    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.object_id IS '--номер объекта. Заполняется только если оплачиваются субподрядные договора';
          public          postgres    false    236            �           0    0 #   COLUMN payments_summary_tab.partner    COMMENT     Q   COMMENT ON COLUMN public.payments_summary_tab.partner IS 'КОНТРАГЕНТ';
          public          postgres    false    236            �           0    0 '   COLUMN payments_summary_tab.payment_sum    COMMENT     V   COMMENT ON COLUMN public.payments_summary_tab.payment_sum IS 'ОБЩАЯ СУММА';
          public          postgres    false    236            �           0    0 &   COLUMN payments_summary_tab.payment_at    COMMENT     Y   COMMENT ON COLUMN public.payments_summary_tab.payment_at IS 'ДАТА СОЗДАНИЯ';
          public          postgres    false    236            �           0    0 ,   COLUMN payments_summary_tab.payment_due_date    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.payment_due_date IS 'СРОК ОПЛАТЫ';
          public          postgres    false    236            �           0    0 6   COLUMN payments_summary_tab.payment_full_agreed_status    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.payment_full_agreed_status IS 'СОХРАНИТЬ ДО ПОЛНОЙ ОПЛАТЫ';
          public          postgres    false    236            �           0    0 )   COLUMN payments_summary_tab.payment_owner    COMMENT     b   COMMENT ON COLUMN public.payments_summary_tab.payment_owner IS 'СОЗДАТЕЛЬ ЗАЯВКИ';
          public          postgres    false    236            �           0    0 '   COLUMN payments_summary_tab.responsible    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.responsible IS 'ОТВЕТСТВЕННЫЙ';
          public          postgres    false    236            �           0    0 *   COLUMN payments_summary_tab.payment_status    COMMENT     _   COMMENT ON COLUMN public.payments_summary_tab.payment_status IS '--статус заявки';
          public          postgres    false    236            �            1259    32863 #   payments_summary_tab_payment_id_seq    SEQUENCE     �   ALTER TABLE public.payments_summary_tab ALTER COLUMN payment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_summary_tab_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    236            �            1259    16480 	   user_role    TABLE     �   CREATE TABLE public.user_role (
    role_id smallint NOT NULL,
    role_name text NOT NULL,
    role_priority smallint NOT NULL
);
    DROP TABLE public.user_role;
       public         heap    postgres    false            �           0    0    TABLE user_role    COMMENT     m   COMMENT ON TABLE public.user_role IS 'Список ролей пользователей в системе';
          public          postgres    false    234            �           0    0    COLUMN user_role.role_priority    COMMENT     �   COMMENT ON COLUMN public.user_role.role_priority IS 'Приоритет роли. Роме нужны цифра для разграничения прав на фронтенде';
          public          postgres    false    234            �            1259    16479    user_role_role_id_seq    SEQUENCE     �   ALTER TABLE public.user_role ALTER COLUMN role_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_role_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    234            �            1259    16444    users    TABLE     �  CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    user_priority smallint NOT NULL,
    password text NOT NULL,
    user_role_id smallint NOT NULL,
    is_fired boolean DEFAULT false NOT NULL,
    employment_date date DEFAULT CURRENT_TIMESTAMP NOT NULL,
    date_of_dismissal date
);
    DROP TABLE public.users;
       public         heap    postgres    false            �           0    0    COLUMN users.employment_date    COMMENT     ]   COMMENT ON COLUMN public.users.employment_date IS 'Дата приёма на работу';
          public          postgres    false    229            �           0    0    COLUMN users.date_of_dismissal    COMMENT     U   COMMENT ON COLUMN public.users.date_of_dismissal IS 'Дата увольнения';
          public          postgres    false    229            �           0    0    TABLE users    ACL     .   GRANT ALL ON TABLE public.users TO kpln_user;
          public          postgres    false    229            �            1259    16450    users_user_id_seq    SEQUENCE     �   ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    229            �           0    0    SEQUENCE users_user_id_seq    ACL     =   GRANT ALL ON SEQUENCE public.users_user_id_seq TO kpln_user;
          public          postgres    false    230            �            1259    16451    vat    TABLE     �   CREATE TABLE public.vat (
    vat_id smallint NOT NULL,
    vat_name text NOT NULL,
    vat_value real GENERATED ALWAYS AS (
CASE vat_name
    WHEN 'с НДС'::text THEN 1.2
    ELSE (1)::numeric
END) STORED NOT NULL
);
    DROP TABLE public.vat;
       public         heap    postgres    false            �           0    0 	   TABLE vat    COMMENT     )   COMMENT ON TABLE public.vat IS 'НДС';
          public          postgres    false    231            �           0    0 	   TABLE vat    ACL     ,   GRANT ALL ON TABLE public.vat TO kpln_user;
          public          postgres    false    231            �            1259    16457    vat_vat_id_seq    SEQUENCE     �   ALTER TABLE public.vat ALTER COLUMN vat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.vat_vat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    231            �           0    0    SEQUENCE vat_vat_id_seq    ACL     :   GRANT ALL ON SEQUENCE public.vat_vat_id_seq TO kpln_user;
          public          postgres    false    232            t          0    16399    contract_purposes 
   TABLE DATA           W   COPY public.contract_purposes (contract_purpose_id, contract_purpose_name) FROM stdin;
    public          postgres    false    214   Я       v          0    16405    contract_statuses 
   TABLE DATA           U   COPY public.contract_statuses (contract_status_id, contract_status_name) FROM stdin;
    public          postgres    false    216   �       x          0    16411    contract_types 
   TABLE DATA           N   COPY public.contract_types (contract_type_id, contract_type_name) FROM stdin;
    public          postgres    false    218   i�       |          0    16424 	   contracts 
   TABLE DATA           �   COPY public.contracts (contract_id, contract_name, stage, department, contract_number, created_at, start_date, costs) FROM stdin;
    public          postgres    false    222   ��       ~          0    16431    new_objects 
   TABLE DATA           �   COPY public.new_objects (object_id, object_name, contract_type, date_row, contract_number, customer, contractor, contract_comment, contract_status, contract_purpose, vat, vat_value) FROM stdin;
    public          postgres    false    224   �       �          0    16438    objects 
   TABLE DATA           9   COPY public.objects (object_id, object_name) FROM stdin;
    public          postgres    false    227   %�       z          0    16417    our_companies 
   TABLE DATA           L   COPY public.our_companies (contractor_id, contractor_name, vat) FROM stdin;
    public          postgres    false    220   s�       �          0    32872    payment_agreed_statuses 
   TABLE DATA           �   COPY public.payment_agreed_statuses (payment_agreed_status_id, payment_agreed_status_name, payment_agreed_status_category) FROM stdin;
    public          postgres    false    237   ò       �          0    32950    payment_cost_items 
   TABLE DATA           ^   COPY public.payment_cost_items (cost_item_id, cost_item_name, cost_item_category) FROM stdin;
    public          postgres    false    242   ��       �          0    33001    payments_andrew_statuses 
   TABLE DATA           w   COPY public.payments_andrew_statuses (payment_andrew_status_id, payment_id, status_id, user_id, create_at) FROM stdin;
    public          postgres    false    244   �       �          0    32922    payments_approval 
   TABLE DATA           �   COPY public.payments_approval (payment_approval_id, payment_id, payment_approval_status_id, payment_approval_date, payment_approval_sum) FROM stdin;
    public          postgres    false    239   t�       �          0    32942    payments_paid 
   TABLE DATA           �   COPY public.payments_paid (payment_pay_id, payment_id, payment_paid_status_id, payment_full_paid_status, payment_paid_sum) FROM stdin;
    public          postgres    false    241   ��       �          0    32864    payments_summary_tab 
   TABLE DATA             COPY public.payments_summary_tab (payment_id, our_companies_id, cost_item_id, payment_number, basis_of_payment, payment_description, object_id, partner, payment_sum, payment_at, payment_due_date, payment_full_agreed_status, payment_owner, responsible, payment_status) FROM stdin;
    public          postgres    false    236   ��       �          0    16480 	   user_role 
   TABLE DATA           F   COPY public.user_role (role_id, role_name, role_priority) FROM stdin;
    public          postgres    false    234   0�       �          0    16444    users 
   TABLE DATA           �   COPY public.users (user_id, first_name, last_name, email, created_at, user_priority, password, user_role_id, is_fired, employment_date, date_of_dismissal) FROM stdin;
    public          postgres    false    229   ��       �          0    16451    vat 
   TABLE DATA           /   COPY public.vat (vat_id, vat_name) FROM stdin;
    public          postgres    false    231   ��       �           0    0 (   contract_purposes_contract_purpos_id_seq    SEQUENCE SET     V   SELECT pg_catalog.setval('public.contract_purposes_contract_purpos_id_seq', 2, true);
          public          postgres    false    215            �           0    0 (   contract_statuses_contract_status_id_seq    SEQUENCE SET     V   SELECT pg_catalog.setval('public.contract_statuses_contract_status_id_seq', 3, true);
          public          postgres    false    217            �           0    0 #   contract_types_contract_type_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public.contract_types_contract_type_id_seq', 2, true);
          public          postgres    false    219            �           0    0    contractors_contractor_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.contractors_contractor_id_seq', 4, true);
          public          postgres    false    221            �           0    0    contracts_contracts_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.contracts_contracts_id_seq', 1, true);
          public          postgres    false    223            �           0    0    new_objects_object_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.new_objects_object_id_seq', 1, false);
          public          postgres    false    225            �           0    0    new_objects_object_id_seq1    SEQUENCE SET     I   SELECT pg_catalog.setval('public.new_objects_object_id_seq1', 29, true);
          public          postgres    false    226            �           0    0    objects_object_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.objects_object_id_seq', 2, true);
          public          postgres    false    228            �           0    0 #   payment_cost_items_cost_item_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.payment_cost_items_cost_item_id_seq', 36, true);
          public          postgres    false    243            �           0    0 %   payments_agreed_payment_agreed_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.payments_agreed_payment_agreed_id_seq', 1, false);
          public          postgres    false    238            �           0    0 5   payments_andrew_statuses_payment_andrew_status_id_seq    SEQUENCE SET     c   SELECT pg_catalog.setval('public.payments_andrew_statuses_payment_andrew_status_id_seq', 6, true);
          public          postgres    false    245            �           0    0     payments_paid_payment_pay_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.payments_paid_payment_pay_id_seq', 1, false);
          public          postgres    false    240            �           0    0 #   payments_summary_tab_payment_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.payments_summary_tab_payment_id_seq', 28, true);
          public          postgres    false    235            �           0    0    user_role_role_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.user_role_role_id_seq', 5, true);
          public          postgres    false    233            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 10, true);
          public          postgres    false    230            �           0    0    vat_vat_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.vat_vat_id_seq', 2, true);
          public          postgres    false    232            �           2606    16459 (   contract_purposes contract_purposes_pkey 
   CONSTRAINT     w   ALTER TABLE ONLY public.contract_purposes
    ADD CONSTRAINT contract_purposes_pkey PRIMARY KEY (contract_purpose_id);
 R   ALTER TABLE ONLY public.contract_purposes DROP CONSTRAINT contract_purposes_pkey;
       public            postgres    false    214            �           2606    16461 (   contract_statuses contract_statuses_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.contract_statuses
    ADD CONSTRAINT contract_statuses_pkey PRIMARY KEY (contract_status_id);
 R   ALTER TABLE ONLY public.contract_statuses DROP CONSTRAINT contract_statuses_pkey;
       public            postgres    false    216            �           2606    16463 "   contract_types contract_types_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.contract_types
    ADD CONSTRAINT contract_types_pkey PRIMARY KEY (contract_type_id);
 L   ALTER TABLE ONLY public.contract_types DROP CONSTRAINT contract_types_pkey;
       public            postgres    false    218            �           2606    16465    our_companies contractors_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.our_companies
    ADD CONSTRAINT contractors_pkey PRIMARY KEY (contractor_id);
 H   ALTER TABLE ONLY public.our_companies DROP CONSTRAINT contractors_pkey;
       public            postgres    false    220            �           2606    16467    contracts contracts_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (contract_id);
 B   ALTER TABLE ONLY public.contracts DROP CONSTRAINT contracts_pkey;
       public            postgres    false    222            �           2606    16469 +   new_objects new_objects_contract_number_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.new_objects
    ADD CONSTRAINT new_objects_contract_number_key UNIQUE (contract_number);
 U   ALTER TABLE ONLY public.new_objects DROP CONSTRAINT new_objects_contract_number_key;
       public            postgres    false    224            �           2606    16471    new_objects new_objects_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.new_objects
    ADD CONSTRAINT new_objects_pkey PRIMARY KEY (object_id);
 F   ALTER TABLE ONLY public.new_objects DROP CONSTRAINT new_objects_pkey;
       public            postgres    false    224            �           2606    32890    objects objects_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (object_id);
 >   ALTER TABLE ONLY public.objects DROP CONSTRAINT objects_pkey;
       public            postgres    false    227            �           2606    32960 *   payment_cost_items payment_cost_items_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.payment_cost_items
    ADD CONSTRAINT payment_cost_items_pkey PRIMARY KEY (cost_item_id);
 T   ALTER TABLE ONLY public.payment_cost_items DROP CONSTRAINT payment_cost_items_pkey;
       public            postgres    false    242            �           2606    32898 -   payment_agreed_statuses payment_statuses_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.payment_agreed_statuses
    ADD CONSTRAINT payment_statuses_pkey PRIMARY KEY (payment_agreed_status_id);
 W   ALTER TABLE ONLY public.payment_agreed_statuses DROP CONSTRAINT payment_statuses_pkey;
       public            postgres    false    237            �           2606    32928 &   payments_approval payments_agreed_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY public.payments_approval
    ADD CONSTRAINT payments_agreed_pkey PRIMARY KEY (payment_approval_id);
 P   ALTER TABLE ONLY public.payments_approval DROP CONSTRAINT payments_agreed_pkey;
       public            postgres    false    239            �           2606    33006 6   payments_andrew_statuses payments_andrew_statuses_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.payments_andrew_statuses
    ADD CONSTRAINT payments_andrew_statuses_pkey PRIMARY KEY (payment_andrew_status_id);
 `   ALTER TABLE ONLY public.payments_andrew_statuses DROP CONSTRAINT payments_andrew_statuses_pkey;
       public            postgres    false    244            �           2606    32947     payments_paid payments_paid_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.payments_paid
    ADD CONSTRAINT payments_paid_pkey PRIMARY KEY (payment_id);
 J   ALTER TABLE ONLY public.payments_paid DROP CONSTRAINT payments_paid_pkey;
       public            postgres    false    241            �           2606    32907 .   payments_summary_tab payments_summary_tab_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT payments_summary_tab_pkey PRIMARY KEY (payment_id);
 X   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT payments_summary_tab_pkey;
       public            postgres    false    236            �           2606    16486    user_role user_role_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT user_role_pkey PRIMARY KEY (role_id);
 B   ALTER TABLE ONLY public.user_role DROP CONSTRAINT user_role_pkey;
       public            postgres    false    234            �           2606    16475    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    229            �           2606    16477    vat vat_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.vat
    ADD CONSTRAINT vat_pkey PRIMARY KEY (vat_id);
 6   ALTER TABLE ONLY public.vat DROP CONSTRAINT vat_pkey;
       public            postgres    false    231            �           2606    32976 !   payments_summary_tab fk_cost_item    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_cost_item FOREIGN KEY (cost_item_id) REFERENCES public.payment_cost_items(cost_item_id) NOT VALID;
 K   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_cost_item;
       public          postgres    false    236    242    3290            �           2606    32981 !   payments_summary_tab fk_object_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_object_id FOREIGN KEY (object_id) REFERENCES public.objects(object_id) NOT VALID;
 K   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_object_id;
       public          postgres    false    227    236    3274            �           2606    32971 #   payments_summary_tab fk_our_company    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_our_company FOREIGN KEY (our_companies_id) REFERENCES public.our_companies(contractor_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_our_company;
       public          postgres    false    220    236    3266            �           2606    32961 %   payments_summary_tab fk_payment_owner    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_payment_owner FOREIGN KEY (payment_owner) REFERENCES public.users(user_id) NOT VALID;
 O   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_payment_owner;
       public          postgres    false    3276    229    236            �           2606    32966 #   payments_summary_tab fk_responsible    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_responsible FOREIGN KEY (responsible) REFERENCES public.users(user_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_responsible;
       public          postgres    false    3276    229    236            �           2606    32986    users fk_user_role    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_user_role FOREIGN KEY (user_role_id) REFERENCES public.user_role(role_id) NOT VALID;
 <   ALTER TABLE ONLY public.users DROP CONSTRAINT fk_user_role;
       public          postgres    false    234    3280    229            �           2606    33007 #   payments_andrew_statuses paymant_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_andrew_statuses
    ADD CONSTRAINT paymant_id FOREIGN KEY (payment_id) REFERENCES public.payments_summary_tab(payment_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_andrew_statuses DROP CONSTRAINT paymant_id;
       public          postgres    false    3282    244    236            �           2606    33017 "   payments_andrew_statuses status_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_andrew_statuses
    ADD CONSTRAINT status_id FOREIGN KEY (status_id) REFERENCES public.payment_agreed_statuses(payment_agreed_status_id) NOT VALID;
 L   ALTER TABLE ONLY public.payments_andrew_statuses DROP CONSTRAINT status_id;
       public          postgres    false    237    3284    244            �           2606    33012     payments_andrew_statuses user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_andrew_statuses
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 J   ALTER TABLE ONLY public.payments_andrew_statuses DROP CONSTRAINT user_id;
       public          postgres    false    229    3276    244            t   2   x�3估�b���.v_�taÅ�@V��~.#�s/lU�،U6F��� oI#A      v   G   x�3�0�¾[.쿰�b��rq^X�pa:����_l����2漰��֋�5l	r��qqq �(`      x   ,   x�3�0�¾���]�ra���;��8/,���b#�`� ��      |   3   x�3�4�B##c]s]C#C3+s+SK=#sS3smc�,P)W� �	�      ~   -  x���MN�0���)���-�]�ğ�1��c�q$n�I�!#x��W�$~e�B����=yir�&�n�7k��|� \�1'h���+T���A<�!}_Ex����%�(P��O��6$�v�'J�rsMx2g\�x�W���Rj�dR��������t0Dry���z~���w����(�%=������v�T���a͒poV&��(���N��:�p8���9�h2�T��PKZL��-H�%�K�ؗS��~���U�����THR���κ����� ǒ�%��[�����<����      �   >   x�3 ��1	Снт. Клязьма
2	Мытищи 35 39
\.


���      z   @   x�3�0����/��,�2⼰��9Ӹ���
�%@)����/�_�qa��!P(F��� �HM      �   �   x���;
AD�S�	��z`"hj`"f�k` ��hf:����B���YX0îz����1*�x"C.��b�ܘ����y�aOp&Z�2jAr�ھ/�Z�NMP�֔���鱅������^��
n�NO߽k�Q�4�������(��ŋ?��!`|�l�Yd�� ��w      �   u  x��U�n�@}^�>&R�JL��A+��16iK+���Vj�6!D�c��`��a��rfl�ZQ����9s;3K[�/�.��r<cw���ϱw�螦�ҍ�Җb�'��\�J��+�	'�Ÿ�9V4�{�ô�6d�hZP��]�?}1�.$Ck�S�.������e����2Č{������*z� ��Д#I��)��"��3&k~��h�p��t�z���� �9!�Ȝhı n8c2<W��(�-g��!�9:'��4*��ڝD���S������]��	�T���D��Ñ�v�)?V� �)x[7liȻ(:��i��jлLİ�ྡྷ	��ְ�Ҋ�9G�d��*�"���=w1pK�G֥��'�f�E� e��<�}-u*�7Hm�!�C�ǍOw�ϡ�uQ��x���;�f9Z�ZRGV��D�e� �(
ٯ�K1l�8-L�Ζ�@ԕ��81�Ņ�e)�^f#�	��h��-)��>F�"�^�FJ�c��$�y����1��S��1�O �Z/8������W�~�m����o/-s��t���&�y�6�|Gqax�ªq���I�pM 3��7>��zV��;�+��J���U�ߴ<�{,�r      �   _   x�m̱�0�ڙ�%�����,�?	���N	��@`he��Cz��i����d-�>l$#�[��]7���[&m��7[��c����s�Z)��o>      �      x������ � �      �      x������ � �      �   r  x�u�=N�@���)F�@`k{� Z��P��&�"E@B�$��4�Cs��+p�M"9(xmkf���7OGB�D���*Jd)m��#�y�O<�������t$x���u8��<询u,������BKm|�:&�LM��&06N�9��V�B�H\�]zHֆ��H�)�1�otw危 ��I	�:%MA<ェ�&\�������!1�O�~���u\�_��A8����Jђ�0a�l��V�a��oˈ'T����FôlF��'(��ǲ5.� ��/��X�����:�������B����ܒ
S%S��Dǉ�[�ۺ�����F���<�e>"�P��Me�;���=�h�n0�J0ec�LW`����P;�      �   G   x�3�LL����4�2�L�,JM.�/�4�2��I,�L-�4�2�,-2��9SRJ�3RS8��b���� P�      �   d  x����jA��=O���$C�Su�N��5�$F2���ԕ4s1�2�[�\��@B$�3t��j�D�0�Mw5�����C{�~i\}�?۳��������B�rU�U�+@��Z�E��w���:�㘱>>pH�֢{�OF����tN�P?x��(�S0.� A��i�,��J!��H2�� ����v>t�(h���=]�����%�y{q���^�&�6��L
��z�X�F�A�&F�A�b��-}�==~3�9:����.��e�Q����cɞ<{
&f�������堛����]K��(�
��h����=twwp�ַ(����dmKT�!c��V
J)Z�NyCB"r�YdfR�Â����t��}`-����7�ۧ�[�`���zԏ �t�S�Kl
9�S2Cy�21F��␭ �>�dPyD)D��T�~����Ҙ�%��_���I�5�ѿE?�Z���,�39i^�9�x5�>�9�f*�ڢ7>���Ҏ<٬}R"Je�Q���)"�2���� n��ޠV k�`���ҫ-o63=�����F����-a�	�<Z�T��Q]pG�Ke�^��冄�&A�ٱfa���^�M�g�      �   $   x�3�بpa�)rq^�xa��0~� ��     