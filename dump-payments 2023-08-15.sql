PGDMP                         {            kpln_db    15.3    15.3 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24576    kpln_db    DATABASE     {   CREATE DATABASE kpln_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE kpln_db;
                postgres    false            �            1259    24577    contract_purposes    TABLE     }   CREATE TABLE public.contract_purposes (
    contract_purpose_id integer NOT NULL,
    contract_purpose_name text NOT NULL
);
 %   DROP TABLE public.contract_purposes;
       public         heap    postgres    false            �           0    0    TABLE contract_purposes    COMMENT     |   COMMENT ON TABLE public.contract_purposes IS 'Назначения (Учитывается / Не учитывается)';
          public          postgres    false    214            �            1259    24582 (   contract_purposes_contract_purpos_id_seq    SEQUENCE     �   ALTER TABLE public.contract_purposes ALTER COLUMN contract_purpose_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_purposes_contract_purpos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    214            �            1259    24583    contract_statuses    TABLE     {   CREATE TABLE public.contract_statuses (
    contract_status_id integer NOT NULL,
    contract_status_name text NOT NULL
);
 %   DROP TABLE public.contract_statuses;
       public         heap    postgres    false            �            1259    24588 (   contract_statuses_contract_status_id_seq    SEQUENCE     �   ALTER TABLE public.contract_statuses ALTER COLUMN contract_status_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_statuses_contract_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �            1259    24589    contract_types    TABLE     t   CREATE TABLE public.contract_types (
    contract_type_id integer NOT NULL,
    contract_type_name text NOT NULL
);
 "   DROP TABLE public.contract_types;
       public         heap    postgres    false            �            1259    24594 #   contract_types_contract_type_id_seq    SEQUENCE     �   ALTER TABLE public.contract_types ALTER COLUMN contract_type_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contract_types_contract_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    218            �            1259    24595    our_companies    TABLE     <  CREATE TABLE public.our_companies (
    contractor_id integer NOT NULL,
    contractor_name text NOT NULL,
    vat boolean DEFAULT true NOT NULL,
    contractor_value real GENERATED ALWAYS AS (
CASE
    WHEN vat THEN 1.2
    ELSE (1)::numeric
END) STORED NOT NULL,
    inflow_active boolean DEFAULT true NOT NULL
);
 !   DROP TABLE public.our_companies;
       public         heap    postgres    false            �           0    0    TABLE our_companies    COMMENT     U   COMMENT ON TABLE public.our_companies IS 'Список наших компаний';
          public          postgres    false    220            �           0    0 $   COLUMN our_companies.contractor_name    COMMENT     ^   COMMENT ON COLUMN public.our_companies.contractor_name IS 'Названиекомпании';
          public          postgres    false    220            �           0    0    COLUMN our_companies.vat    COMMENT     �   COMMENT ON COLUMN public.our_companies.vat IS 'начисление НДС при расчетах (по умолчанию да)';
          public          postgres    false    220            �           0    0 %   COLUMN our_companies.contractor_value    COMMENT     �   COMMENT ON COLUMN public.our_companies.contractor_value IS 'Коэффициент НДС. Автоматически рассчитывается. Если НДС = true, то 1.2, иначе 1';
          public          postgres    false    220            �           0    0 "   COLUMN our_companies.inflow_active    COMMENT     �   COMMENT ON COLUMN public.our_companies.inflow_active IS 'Компания доступна для внесения платежей и пополнения баланса';
          public          postgres    false    220            �            1259    24601    contractors_contractor_id_seq    SEQUENCE     �   ALTER TABLE public.our_companies ALTER COLUMN contractor_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contractors_contractor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    220            �            1259    24602 	   contracts    TABLE     q  CREATE TABLE public.contracts (
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
       public         heap    postgres    false            �            1259    24608    contracts_contracts_id_seq    SEQUENCE     �   ALTER TABLE public.contracts ALTER COLUMN contract_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contracts_contracts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    222            �            1259    32846    payment_draft    TABLE       CREATE TABLE public.payment_draft (
    draft_id integer NOT NULL,
    page_name text NOT NULL,
    parent_id text,
    parameter_name text NOT NULL,
    parameter_value text NOT NULL,
    user_id bigint,
    create_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
 !   DROP TABLE public.payment_draft;
       public         heap    postgres    false            �           0    0    TABLE payment_draft    COMMENT     a  COMMENT ON TABLE public.payment_draft IS 'Таблица с временными значениями, внесенными в ячейки. но не сохраненные в основные поля ввода.
Например для страницы payment_approval_3  сохраняем значение "Согласованная сумма';
          public          postgres    false    247            �           0    0    COLUMN payment_draft.page_name    COMMENT     �   COMMENT ON COLUMN public.payment_draft.page_name IS 'Название странице, где используют данные';
          public          postgres    false    247            �           0    0    COLUMN payment_draft.parent_id    COMMENT     �   COMMENT ON COLUMN public.payment_draft.parent_id IS 'идентинтификатор сущности (номер строки, id заявки и прочее), чей параметр получает временные значений';
          public          postgres    false    247            �           0    0 #   COLUMN payment_draft.parameter_name    COMMENT     �   COMMENT ON COLUMN public.payment_draft.parameter_name IS 'Наименвоание параметра, для которого задаётся временное значение';
          public          postgres    false    247            �           0    0 $   COLUMN payment_draft.parameter_value    COMMENT     t   COMMENT ON COLUMN public.payment_draft.parameter_value IS 'Временное значение параметра';
          public          postgres    false    247            �           0    0    COLUMN payment_draft.user_id    COMMENT     �   COMMENT ON COLUMN public.payment_draft.user_id IS 'Пользователь, для которого отображается значение';
          public          postgres    false    247            �           0    0    COLUMN payment_draft.create_at    COMMENT     Q   COMMENT ON COLUMN public.payment_draft.create_at IS 'дата создания';
          public          postgres    false    247            �            1259    32845    draft_payment_draft_id_seq    SEQUENCE     �   ALTER TABLE public.payment_draft ALTER COLUMN draft_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.draft_payment_draft_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    247            �            1259    24609    new_objects    TABLE     �  CREATE TABLE public.new_objects (
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
       public         heap    postgres    false            �            1259    24614    new_objects_object_id_seq    SEQUENCE     �   CREATE SEQUENCE public.new_objects_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.new_objects_object_id_seq;
       public          postgres    false    224            �           0    0    new_objects_object_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.new_objects_object_id_seq OWNED BY public.new_objects.object_id;
          public          postgres    false    225            �            1259    24615    new_objects_object_id_seq1    SEQUENCE     �   ALTER TABLE public.new_objects ALTER COLUMN object_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.new_objects_object_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    224            �            1259    24616    objects    TABLE     l   CREATE TABLE public.objects (
    object_id integer NOT NULL,
    object_name character varying NOT NULL
);
    DROP TABLE public.objects;
       public         heap    postgres    false            �            1259    24621    objects_object_id_seq    SEQUENCE     �   ALTER TABLE public.objects ALTER COLUMN object_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.objects_object_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    227            �            1259    24622    payment_agreed_statuses    TABLE     �   CREATE TABLE public.payment_agreed_statuses (
    payment_agreed_status_id smallint NOT NULL,
    payment_agreed_status_name text NOT NULL,
    payment_agreed_status_category text NOT NULL
);
 +   DROP TABLE public.payment_agreed_statuses;
       public         heap    postgres    false            �           0    0    TABLE payment_agreed_statuses    COMMENT     �  COMMENT ON TABLE public.payment_agreed_statuses IS 'Статусы платежей. Различаются категориями:
Статусы Андрея - статусы согласования - "Черновик / "Реком." / "Аннулирован" / "К рассмотрению"
Статусы оплаты - "В оплате" / "Полная оплата" / "Частичная оплата"';
          public          postgres    false    229            �            1259    24627    payment_cost_items    TABLE     �   CREATE TABLE public.payment_cost_items (
    cost_item_id smallint NOT NULL,
    cost_item_name text NOT NULL,
    cost_item_category text NOT NULL
);
 &   DROP TABLE public.payment_cost_items;
       public         heap    postgres    false            �           0    0    TABLE payment_cost_items    COMMENT     a   COMMENT ON TABLE public.payment_cost_items IS 'СТАТЬЯ ЗАТРАТ (ТИП ЗАЯВКИ)';
          public          postgres    false    230            �            1259    24632 #   payment_cost_items_cost_item_id_seq    SEQUENCE     �   ALTER TABLE public.payment_cost_items ALTER COLUMN cost_item_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payment_cost_items_cost_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    230            �            1259    32860    payment_inflow_type    TABLE     v   CREATE TABLE public.payment_inflow_type (
    inflow_type_id smallint NOT NULL,
    inflow_type_name text NOT NULL
);
 '   DROP TABLE public.payment_inflow_type;
       public         heap    postgres    false            �           0    0    TABLE payment_inflow_type    COMMENT       COMMENT ON TABLE public.payment_inflow_type IS 'Таблица со списком значений параметра "ТИП ПОСТУПЛЕНИЯ"
"Поступление ДС", "П.О.", "Корректирующий платеж", "Внутренний платеж"';
          public          postgres    false    249            �            1259    32859 &   payment_inflow_type_inflow_type_id_seq    SEQUENCE     �   ALTER TABLE public.payment_inflow_type ALTER COLUMN inflow_type_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payment_inflow_type_inflow_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    249            �            1259    24633    payments_approval    TABLE     �   CREATE TABLE public.payments_approval (
    id smallint NOT NULL,
    payment_id smallint NOT NULL,
    approval_at time with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approval_sum numeric(9,2) NOT NULL,
    confirm_id smallint NOT NULL
);
 %   DROP TABLE public.payments_approval;
       public         heap    postgres    false            �           0    0    TABLE payments_approval    COMMENT     �   COMMENT ON TABLE public.payments_approval IS 'Статусы одобрения платежей Андреем
Только не оплаченные полностью платежи';
          public          postgres    false    232            �           0    0    COLUMN payments_approval.id    COMMENT     _   COMMENT ON COLUMN public.payments_approval.id IS 'id согласования платежа';
          public          postgres    false    232            �           0    0 #   COLUMN payments_approval.payment_id    COMMENT     k   COMMENT ON COLUMN public.payments_approval.payment_id IS 'id согласованного платежа';
          public          postgres    false    232            �           0    0 $   COLUMN payments_approval.approval_at    COMMENT     k   COMMENT ON COLUMN public.payments_approval.approval_at IS 'Время внесения в таблицу';
          public          postgres    false    232            �           0    0 %   COLUMN payments_approval.approval_sum    COMMENT     l   COMMENT ON COLUMN public.payments_approval.approval_sum IS 'Согласованная стоимость';
          public          postgres    false    232            �           0    0 #   COLUMN payments_approval.confirm_id    COMMENT     z   COMMENT ON COLUMN public.payments_approval.confirm_id IS 'id записи из таблицы payments_approval_history';
          public          postgres    false    232            �            1259    24636 %   payments_agreed_payment_agreed_id_seq    SEQUENCE     �   ALTER TABLE public.payments_approval ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_agreed_payment_agreed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    232            �            1259    24637    payments_approval_history    TABLE        CREATE TABLE public.payments_approval_history (
    confirm_id smallint NOT NULL,
    payment_id smallint NOT NULL,
    status_id smallint NOT NULL,
    user_id smallint NOT NULL,
    create_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approval_sum numeric(9,2)
);
 -   DROP TABLE public.payments_approval_history;
       public         heap    postgres    false            �           0    0    TABLE payments_approval_history    COMMENT     �   COMMENT ON TABLE public.payments_approval_history IS 'История статусов одобрения платежей Андреем
Сохраняются все записи';
          public          postgres    false    234            �           0    0 +   COLUMN payments_approval_history.confirm_id    COMMENT     T   COMMENT ON COLUMN public.payments_approval_history.confirm_id IS 'id записи';
          public          postgres    false    234            �           0    0 +   COLUMN payments_approval_history.payment_id    COMMENT     T   COMMENT ON COLUMN public.payments_approval_history.payment_id IS 'id заявки';
          public          postgres    false    234            �           0    0 *   COLUMN payments_approval_history.status_id    COMMENT     �   COMMENT ON COLUMN public.payments_approval_history.status_id IS 'id статуса заявки (черновки, аннул и тд)';
          public          postgres    false    234            �           0    0 (   COLUMN payments_approval_history.user_id    COMMENT     �   COMMENT ON COLUMN public.payments_approval_history.user_id IS 'id пользователя, согласовавшего заявку';
          public          postgres    false    234            �           0    0 -   COLUMN payments_approval_history.approval_sum    COMMENT     j   COMMENT ON COLUMN public.payments_approval_history.approval_sum IS 'Сумма согласования';
          public          postgres    false    234            �            1259    24641 5   payments_andrew_statuses_payment_andrew_status_id_seq    SEQUENCE     
  ALTER TABLE public.payments_approval_history ALTER COLUMN confirm_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_andrew_statuses_payment_andrew_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    234            �            1259    32892    payments_inflow_history    TABLE     Y  CREATE TABLE public.payments_inflow_history (
    inflow_id bigint NOT NULL,
    inflow_company_id integer NOT NULL,
    inflow_description text NOT NULL,
    inflow_type_id smallint NOT NULL,
    inflow_sum numeric(11,2) NOT NULL,
    inflow_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    inflow_owner smallint NOT NULL
);
 +   DROP TABLE public.payments_inflow_history;
       public         heap    postgres    false            �           0    0    TABLE payments_inflow_history    COMMENT     [   COMMENT ON TABLE public.payments_inflow_history IS 'История внесения ДС';
          public          postgres    false    251            �            1259    32891 %   payments_inflow_history_inflow_id_seq    SEQUENCE     �   ALTER TABLE public.payments_inflow_history ALTER COLUMN inflow_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_inflow_history_inflow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    251            �            1259    24642    payments_paid    TABLE     �   CREATE TABLE public.payments_paid (
    payment_pay_id integer NOT NULL,
    payment_id integer NOT NULL,
    payment_paid_status_id smallint,
    payment_full_paid_status boolean DEFAULT false NOT NULL,
    payment_paid_sum numeric(9,2) NOT NULL
);
 !   DROP TABLE public.payments_paid;
       public         heap    postgres    false            �           0    0    TABLE payments_paid    COMMENT     a   COMMENT ON TABLE public.payments_paid IS 'Таблица оплаченных платежей';
          public          postgres    false    236            �           0    0 +   COLUMN payments_paid.payment_paid_status_id    COMMENT     �   COMMENT ON COLUMN public.payments_paid.payment_paid_status_id IS 'ЗАКРЫТЬ ТОЛЬКО ПОСЛЕ ПОЛНОЙ ОПЛАТЫ';
          public          postgres    false    236            �            1259    24646     payments_paid_payment_pay_id_seq    SEQUENCE     �   ALTER TABLE public.payments_paid ALTER COLUMN payment_pay_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_paid_payment_pay_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    236            �            1259    24647    payments_summary_tab    TABLE     �  CREATE TABLE public.payments_summary_tab (
    payment_id integer NOT NULL,
    our_companies_id smallint NOT NULL,
    cost_item_id smallint NOT NULL,
    payment_number text NOT NULL,
    basis_of_payment text NOT NULL,
    payment_description text NOT NULL,
    object_id smallint,
    partner text,
    payment_sum numeric(11,2) NOT NULL,
    payment_due_date date NOT NULL,
    payment_full_agreed_status boolean DEFAULT false NOT NULL,
    payment_owner smallint,
    responsible smallint NOT NULL,
    payment_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    payment_close_status boolean DEFAULT false NOT NULL
);
 (   DROP TABLE public.payments_summary_tab;
       public         heap    postgres    false            �           0    0    TABLE payments_summary_tab    COMMENT     b   COMMENT ON TABLE public.payments_summary_tab IS 'Сводная таблица платежей';
          public          postgres    false    238            �           0    0 &   COLUMN payments_summary_tab.payment_id    COMMENT     Q   COMMENT ON COLUMN public.payments_summary_tab.payment_id IS '--id заявки';
          public          postgres    false    238            �           0    0 ,   COLUMN payments_summary_tab.our_companies_id    COMMENT     U   COMMENT ON COLUMN public.payments_summary_tab.our_companies_id IS 'СИП/КПЛН';
          public          postgres    false    238            �           0    0 (   COLUMN payments_summary_tab.cost_item_id    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.cost_item_id IS 'СТАТЬЯ ЗАТРАТ';
          public          postgres    false    238            �           0    0 *   COLUMN payments_summary_tab.payment_number    COMMENT     V   COMMENT ON COLUMN public.payments_summary_tab.payment_number IS '№ ПЛАТЕЖА';
          public          postgres    false    238            �           0    0 ,   COLUMN payments_summary_tab.basis_of_payment    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.basis_of_payment IS 'ОСНОВАНИЕ ПЛАТЕЖА, № ДОГОВОРА/ № СЧЁТА';
          public          postgres    false    238            �           0    0 /   COLUMN payments_summary_tab.payment_description    COMMENT     Y   COMMENT ON COLUMN public.payments_summary_tab.payment_description IS 'ОПИСАНИЕ';
          public          postgres    false    238            �           0    0 %   COLUMN payments_summary_tab.object_id    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.object_id IS '--номер объекта. Заполняется только если оплачиваются субподрядные договора';
          public          postgres    false    238            �           0    0 #   COLUMN payments_summary_tab.partner    COMMENT     Q   COMMENT ON COLUMN public.payments_summary_tab.partner IS 'КОНТРАГЕНТ';
          public          postgres    false    238            �           0    0 '   COLUMN payments_summary_tab.payment_sum    COMMENT     V   COMMENT ON COLUMN public.payments_summary_tab.payment_sum IS 'ОБЩАЯ СУММА';
          public          postgres    false    238            �           0    0 ,   COLUMN payments_summary_tab.payment_due_date    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.payment_due_date IS 'СРОК ОПЛАТЫ';
          public          postgres    false    238            �           0    0 6   COLUMN payments_summary_tab.payment_full_agreed_status    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.payment_full_agreed_status IS 'СОХРАНИТЬ ДО ПОЛНОЙ ОПЛАТЫ';
          public          postgres    false    238            �           0    0 )   COLUMN payments_summary_tab.payment_owner    COMMENT     b   COMMENT ON COLUMN public.payments_summary_tab.payment_owner IS 'СОЗДАТЕЛЬ ЗАЯВКИ';
          public          postgres    false    238            �           0    0 '   COLUMN payments_summary_tab.responsible    COMMENT     [   COMMENT ON COLUMN public.payments_summary_tab.responsible IS 'ОТВЕТСТВЕННЫЙ';
          public          postgres    false    238            �           0    0 &   COLUMN payments_summary_tab.payment_at    COMMENT     h   COMMENT ON COLUMN public.payments_summary_tab.payment_at IS '--Дата создания заявки';
          public          postgres    false    238                        0    0 0   COLUMN payments_summary_tab.payment_close_status    COMMENT     �   COMMENT ON COLUMN public.payments_summary_tab.payment_close_status IS 'Статус согласования заявки (открыта заявка/закрыта заявка)
По умолчанию - открыто (false)';
          public          postgres    false    238            �            1259    24655 #   payments_summary_tab_payment_id_seq    SEQUENCE     �   ALTER TABLE public.payments_summary_tab ALTER COLUMN payment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.payments_summary_tab_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    238            �            1259    24656 	   user_role    TABLE     �   CREATE TABLE public.user_role (
    role_id smallint NOT NULL,
    role_name text NOT NULL,
    role_priority smallint NOT NULL
);
    DROP TABLE public.user_role;
       public         heap    postgres    false                       0    0    TABLE user_role    COMMENT     m   COMMENT ON TABLE public.user_role IS 'Список ролей пользователей в системе';
          public          postgres    false    240                       0    0    COLUMN user_role.role_priority    COMMENT     �   COMMENT ON COLUMN public.user_role.role_priority IS 'Приоритет роли. Роме нужны цифра для разграничения прав на фронтенде';
          public          postgres    false    240            �            1259    24661    user_role_role_id_seq    SEQUENCE     �   ALTER TABLE public.user_role ALTER COLUMN role_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_role_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    240            �            1259    24662    users    TABLE     �  CREATE TABLE public.users (
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
       public         heap    postgres    false                       0    0    COLUMN users.employment_date    COMMENT     ]   COMMENT ON COLUMN public.users.employment_date IS 'Дата приёма на работу';
          public          postgres    false    242                       0    0    COLUMN users.date_of_dismissal    COMMENT     U   COMMENT ON COLUMN public.users.date_of_dismissal IS 'Дата увольнения';
          public          postgres    false    242            �            1259    24670    users_user_id_seq    SEQUENCE     �   ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    242            �            1259    24671    vat    TABLE     �   CREATE TABLE public.vat (
    vat_id smallint NOT NULL,
    vat_name text NOT NULL,
    vat_value real GENERATED ALWAYS AS (
CASE vat_name
    WHEN 'с НДС'::text THEN 1.2
    ELSE (1)::numeric
END) STORED NOT NULL
);
    DROP TABLE public.vat;
       public         heap    postgres    false                       0    0 	   TABLE vat    COMMENT     )   COMMENT ON TABLE public.vat IS 'НДС';
          public          postgres    false    244            �            1259    24677    vat_vat_id_seq    SEQUENCE     �   ALTER TABLE public.vat ALTER COLUMN vat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.vat_vat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    244            �          0    24577    contract_purposes 
   TABLE DATA           W   COPY public.contract_purposes (contract_purpose_id, contract_purpose_name) FROM stdin;
    public          postgres    false    214   1�       �          0    24583    contract_statuses 
   TABLE DATA           U   COPY public.contract_statuses (contract_status_id, contract_status_name) FROM stdin;
    public          postgres    false    216   s�       �          0    24589    contract_types 
   TABLE DATA           N   COPY public.contract_types (contract_type_id, contract_type_name) FROM stdin;
    public          postgres    false    218   ��       �          0    24602 	   contracts 
   TABLE DATA           �   COPY public.contracts (contract_id, contract_name, stage, department, contract_number, created_at, start_date, costs) FROM stdin;
    public          postgres    false    222   �       �          0    24609    new_objects 
   TABLE DATA           �   COPY public.new_objects (object_id, object_name, contract_type, date_row, contract_number, customer, contractor, contract_comment, contract_status, contract_purpose, vat, vat_value) FROM stdin;
    public          postgres    false    224   I�       �          0    24616    objects 
   TABLE DATA           9   COPY public.objects (object_id, object_name) FROM stdin;
    public          postgres    false    227   ��       �          0    24595    our_companies 
   TABLE DATA           [   COPY public.our_companies (contractor_id, contractor_name, vat, inflow_active) FROM stdin;
    public          postgres    false    220   �       �          0    24622    payment_agreed_statuses 
   TABLE DATA           �   COPY public.payment_agreed_statuses (payment_agreed_status_id, payment_agreed_status_name, payment_agreed_status_category) FROM stdin;
    public          postgres    false    229   m�       �          0    24627    payment_cost_items 
   TABLE DATA           ^   COPY public.payment_cost_items (cost_item_id, cost_item_name, cost_item_category) FROM stdin;
    public          postgres    false    230   R�       �          0    32846    payment_draft 
   TABLE DATA           |   COPY public.payment_draft (draft_id, page_name, parent_id, parameter_name, parameter_value, user_id, create_at) FROM stdin;
    public          postgres    false    247   ��       �          0    32860    payment_inflow_type 
   TABLE DATA           O   COPY public.payment_inflow_type (inflow_type_id, inflow_type_name) FROM stdin;
    public          postgres    false    249   a�       �          0    24633    payments_approval 
   TABLE DATA           b   COPY public.payments_approval (id, payment_id, approval_at, approval_sum, confirm_id) FROM stdin;
    public          postgres    false    232   ��       �          0    24637    payments_approval_history 
   TABLE DATA           x   COPY public.payments_approval_history (confirm_id, payment_id, status_id, user_id, create_at, approval_sum) FROM stdin;
    public          postgres    false    234   Z�       �          0    32892    payments_inflow_history 
   TABLE DATA           �   COPY public.payments_inflow_history (inflow_id, inflow_company_id, inflow_description, inflow_type_id, inflow_sum, inflow_at, inflow_owner) FROM stdin;
    public          postgres    false    251   ��       �          0    24642    payments_paid 
   TABLE DATA           �   COPY public.payments_paid (payment_pay_id, payment_id, payment_paid_status_id, payment_full_paid_status, payment_paid_sum) FROM stdin;
    public          postgres    false    236   ��       �          0    24647    payments_summary_tab 
   TABLE DATA             COPY public.payments_summary_tab (payment_id, our_companies_id, cost_item_id, payment_number, basis_of_payment, payment_description, object_id, partner, payment_sum, payment_due_date, payment_full_agreed_status, payment_owner, responsible, payment_at, payment_close_status) FROM stdin;
    public          postgres    false    238   ��       �          0    24656 	   user_role 
   TABLE DATA           F   COPY public.user_role (role_id, role_name, role_priority) FROM stdin;
    public          postgres    false    240   ��       �          0    24662    users 
   TABLE DATA           �   COPY public.users (user_id, first_name, last_name, email, created_at, user_priority, password, user_role_id, is_fired, employment_date, date_of_dismissal) FROM stdin;
    public          postgres    false    242   �       �          0    24671    vat 
   TABLE DATA           /   COPY public.vat (vat_id, vat_name) FROM stdin;
    public          postgres    false    244   ��                  0    0 (   contract_purposes_contract_purpos_id_seq    SEQUENCE SET     V   SELECT pg_catalog.setval('public.contract_purposes_contract_purpos_id_seq', 2, true);
          public          postgres    false    215                       0    0 (   contract_statuses_contract_status_id_seq    SEQUENCE SET     V   SELECT pg_catalog.setval('public.contract_statuses_contract_status_id_seq', 3, true);
          public          postgres    false    217                       0    0 #   contract_types_contract_type_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public.contract_types_contract_type_id_seq', 2, true);
          public          postgres    false    219            	           0    0    contractors_contractor_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.contractors_contractor_id_seq', 4, true);
          public          postgres    false    221            
           0    0    contracts_contracts_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.contracts_contracts_id_seq', 1, true);
          public          postgres    false    223                       0    0    draft_payment_draft_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.draft_payment_draft_id_seq', 19, true);
          public          postgres    false    246                       0    0    new_objects_object_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.new_objects_object_id_seq', 1, false);
          public          postgres    false    225                       0    0    new_objects_object_id_seq1    SEQUENCE SET     I   SELECT pg_catalog.setval('public.new_objects_object_id_seq1', 29, true);
          public          postgres    false    226                       0    0    objects_object_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.objects_object_id_seq', 5, true);
          public          postgres    false    228                       0    0 #   payment_cost_items_cost_item_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.payment_cost_items_cost_item_id_seq', 36, true);
          public          postgres    false    231                       0    0 &   payment_inflow_type_inflow_type_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.payment_inflow_type_inflow_type_id_seq', 4, true);
          public          postgres    false    248                       0    0 %   payments_agreed_payment_agreed_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.payments_agreed_payment_agreed_id_seq', 19, true);
          public          postgres    false    233                       0    0 5   payments_andrew_statuses_payment_andrew_status_id_seq    SEQUENCE SET     e   SELECT pg_catalog.setval('public.payments_andrew_statuses_payment_andrew_status_id_seq', 268, true);
          public          postgres    false    235                       0    0 %   payments_inflow_history_inflow_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.payments_inflow_history_inflow_id_seq', 1, false);
          public          postgres    false    250                       0    0     payments_paid_payment_pay_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.payments_paid_payment_pay_id_seq', 1, false);
          public          postgres    false    237                       0    0 #   payments_summary_tab_payment_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.payments_summary_tab_payment_id_seq', 115, true);
          public          postgres    false    239                       0    0    user_role_role_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.user_role_role_id_seq', 5, true);
          public          postgres    false    241                       0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 10, true);
          public          postgres    false    243                       0    0    vat_vat_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.vat_vat_id_seq', 2, true);
          public          postgres    false    245            �           2606    24679 (   contract_purposes contract_purposes_pkey 
   CONSTRAINT     w   ALTER TABLE ONLY public.contract_purposes
    ADD CONSTRAINT contract_purposes_pkey PRIMARY KEY (contract_purpose_id);
 R   ALTER TABLE ONLY public.contract_purposes DROP CONSTRAINT contract_purposes_pkey;
       public            postgres    false    214            �           2606    32872 &   contract_statuses contract_status_name 
   CONSTRAINT     q   ALTER TABLE ONLY public.contract_statuses
    ADD CONSTRAINT contract_status_name UNIQUE (contract_status_name);
 P   ALTER TABLE ONLY public.contract_statuses DROP CONSTRAINT contract_status_name;
       public            postgres    false    216            �           2606    24681 (   contract_statuses contract_statuses_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.contract_statuses
    ADD CONSTRAINT contract_statuses_pkey PRIMARY KEY (contract_status_id);
 R   ALTER TABLE ONLY public.contract_statuses DROP CONSTRAINT contract_statuses_pkey;
       public            postgres    false    216            �           2606    24683 "   contract_types contract_types_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.contract_types
    ADD CONSTRAINT contract_types_pkey PRIMARY KEY (contract_type_id);
 L   ALTER TABLE ONLY public.contract_types DROP CONSTRAINT contract_types_pkey;
       public            postgres    false    218            �           2606    24685    our_companies contractors_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.our_companies
    ADD CONSTRAINT contractors_pkey PRIMARY KEY (contractor_id);
 H   ALTER TABLE ONLY public.our_companies DROP CONSTRAINT contractors_pkey;
       public            postgres    false    220            �           2606    24687    contracts contracts_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (contract_id);
 B   ALTER TABLE ONLY public.contracts DROP CONSTRAINT contracts_pkey;
       public            postgres    false    222                       2606    32852     payment_draft draft_payment_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.payment_draft
    ADD CONSTRAINT draft_payment_pkey PRIMARY KEY (draft_id);
 J   ALTER TABLE ONLY public.payment_draft DROP CONSTRAINT draft_payment_pkey;
       public            postgres    false    247                       2606    32884 $   payment_inflow_type inflow_type_name 
   CONSTRAINT     k   ALTER TABLE ONLY public.payment_inflow_type
    ADD CONSTRAINT inflow_type_name UNIQUE (inflow_type_name);
 N   ALTER TABLE ONLY public.payment_inflow_type DROP CONSTRAINT inflow_type_name;
       public            postgres    false    249            �           2606    24689 +   new_objects new_objects_contract_number_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.new_objects
    ADD CONSTRAINT new_objects_contract_number_key UNIQUE (contract_number);
 U   ALTER TABLE ONLY public.new_objects DROP CONSTRAINT new_objects_contract_number_key;
       public            postgres    false    224            �           2606    24691    new_objects new_objects_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.new_objects
    ADD CONSTRAINT new_objects_pkey PRIMARY KEY (object_id);
 F   ALTER TABLE ONLY public.new_objects DROP CONSTRAINT new_objects_pkey;
       public            postgres    false    224            �           2606    24760    objects object_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.objects
    ADD CONSTRAINT object_name UNIQUE (object_name);
 =   ALTER TABLE ONLY public.objects DROP CONSTRAINT object_name;
       public            postgres    false    227            �           2606    24693    objects objects_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (object_id);
 >   ALTER TABLE ONLY public.objects DROP CONSTRAINT objects_pkey;
       public            postgres    false    227            �           2606    32868 /   our_companies our_companies_contractor_name_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.our_companies
    ADD CONSTRAINT our_companies_contractor_name_key UNIQUE (contractor_name);
 Y   ALTER TABLE ONLY public.our_companies DROP CONSTRAINT our_companies_contractor_name_key;
       public            postgres    false    220            �           2606    32876 2   payment_agreed_statuses payment_agreed_status_name 
   CONSTRAINT     �   ALTER TABLE ONLY public.payment_agreed_statuses
    ADD CONSTRAINT payment_agreed_status_name UNIQUE (payment_agreed_status_name);
 \   ALTER TABLE ONLY public.payment_agreed_statuses DROP CONSTRAINT payment_agreed_status_name;
       public            postgres    false    229            �           2606    24695 *   payment_cost_items payment_cost_items_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.payment_cost_items
    ADD CONSTRAINT payment_cost_items_pkey PRIMARY KEY (cost_item_id);
 T   ALTER TABLE ONLY public.payment_cost_items DROP CONSTRAINT payment_cost_items_pkey;
       public            postgres    false    230                       2606    32866 ,   payment_inflow_type payment_inflow_type_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.payment_inflow_type
    ADD CONSTRAINT payment_inflow_type_pkey PRIMARY KEY (inflow_type_id);
 V   ALTER TABLE ONLY public.payment_inflow_type DROP CONSTRAINT payment_inflow_type_pkey;
       public            postgres    false    249            �           2606    24697 -   payment_agreed_statuses payment_statuses_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.payment_agreed_statuses
    ADD CONSTRAINT payment_statuses_pkey PRIMARY KEY (payment_agreed_status_id);
 W   ALTER TABLE ONLY public.payment_agreed_statuses DROP CONSTRAINT payment_statuses_pkey;
       public            postgres    false    229            �           2606    32823 &   payments_approval payments_agreed_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.payments_approval
    ADD CONSTRAINT payments_agreed_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.payments_approval DROP CONSTRAINT payments_agreed_pkey;
       public            postgres    false    232            �           2606    24701 7   payments_approval_history payments_andrew_statuses_pkey 
   CONSTRAINT     }   ALTER TABLE ONLY public.payments_approval_history
    ADD CONSTRAINT payments_andrew_statuses_pkey PRIMARY KEY (confirm_id);
 a   ALTER TABLE ONLY public.payments_approval_history DROP CONSTRAINT payments_andrew_statuses_pkey;
       public            postgres    false    234            
           2606    32899 4   payments_inflow_history payments_inflow_history_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.payments_inflow_history
    ADD CONSTRAINT payments_inflow_history_pkey PRIMARY KEY (inflow_type_id);
 ^   ALTER TABLE ONLY public.payments_inflow_history DROP CONSTRAINT payments_inflow_history_pkey;
       public            postgres    false    251            �           2606    24703     payments_paid payments_paid_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.payments_paid
    ADD CONSTRAINT payments_paid_pkey PRIMARY KEY (payment_id);
 J   ALTER TABLE ONLY public.payments_paid DROP CONSTRAINT payments_paid_pkey;
       public            postgres    false    236            �           2606    24705 .   payments_summary_tab payments_summary_tab_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT payments_summary_tab_pkey PRIMARY KEY (payment_id);
 X   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT payments_summary_tab_pkey;
       public            postgres    false    238            �           2606    32870    contract_purposes purpose_name 
   CONSTRAINT     j   ALTER TABLE ONLY public.contract_purposes
    ADD CONSTRAINT purpose_name UNIQUE (contract_purpose_name);
 H   ALTER TABLE ONLY public.contract_purposes DROP CONSTRAINT purpose_name;
       public            postgres    false    214            �           2606    32886    user_role role_name 
   CONSTRAINT     S   ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT role_name UNIQUE (role_name);
 =   ALTER TABLE ONLY public.user_role DROP CONSTRAINT role_name;
       public            postgres    false    240            �           2606    32874    contract_types type_name 
   CONSTRAINT     a   ALTER TABLE ONLY public.contract_types
    ADD CONSTRAINT type_name UNIQUE (contract_type_name);
 B   ALTER TABLE ONLY public.contract_types DROP CONSTRAINT type_name;
       public            postgres    false    218            �           2606    24707    user_role user_role_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT user_role_pkey PRIMARY KEY (role_id);
 B   ALTER TABLE ONLY public.user_role DROP CONSTRAINT user_role_pkey;
       public            postgres    false    240            �           2606    32888    users users_email 
   CONSTRAINT     M   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email UNIQUE (email);
 ;   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email;
       public            postgres    false    242            �           2606    24709    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    242                        2606    32890    vat vat_name 
   CONSTRAINT     I   ALTER TABLE ONLY public.vat
    ADD CONSTRAINT vat_name UNIQUE (vat_id);
 6   ALTER TABLE ONLY public.vat DROP CONSTRAINT vat_name;
       public            postgres    false    244                       2606    24711    vat vat_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.vat
    ADD CONSTRAINT vat_pkey PRIMARY KEY (vat_id);
 6   ALTER TABLE ONLY public.vat DROP CONSTRAINT vat_pkey;
       public            postgres    false    244                       2606    32838    payments_approval confirm_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_approval
    ADD CONSTRAINT confirm_id FOREIGN KEY (confirm_id) REFERENCES public.payments_approval_history(confirm_id) NOT VALID;
 F   ALTER TABLE ONLY public.payments_approval DROP CONSTRAINT confirm_id;
       public          postgres    false    232    234    3314                       2606    24712 !   payments_summary_tab fk_cost_item    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_cost_item FOREIGN KEY (cost_item_id) REFERENCES public.payment_cost_items(cost_item_id) NOT VALID;
 K   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_cost_item;
       public          postgres    false    3310    238    230                       2606    24717 !   payments_summary_tab fk_object_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_object_id FOREIGN KEY (object_id) REFERENCES public.objects(object_id) NOT VALID;
 K   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_object_id;
       public          postgres    false    3304    238    227                       2606    24722 #   payments_summary_tab fk_our_company    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_our_company FOREIGN KEY (our_companies_id) REFERENCES public.our_companies(contractor_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_our_company;
       public          postgres    false    3292    238    220                       2606    24727 %   payments_summary_tab fk_payment_owner    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_payment_owner FOREIGN KEY (payment_owner) REFERENCES public.users(user_id) NOT VALID;
 O   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_payment_owner;
       public          postgres    false    3326    238    242                       2606    24732 #   payments_summary_tab fk_responsible    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_summary_tab
    ADD CONSTRAINT fk_responsible FOREIGN KEY (responsible) REFERENCES public.users(user_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_summary_tab DROP CONSTRAINT fk_responsible;
       public          postgres    false    3326    238    242                       2606    24737    users fk_user_role    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_user_role FOREIGN KEY (user_role_id) REFERENCES public.user_role(role_id) NOT VALID;
 <   ALTER TABLE ONLY public.users DROP CONSTRAINT fk_user_role;
       public          postgres    false    3322    242    240                       2606    24742 $   payments_approval_history paymant_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_approval_history
    ADD CONSTRAINT paymant_id FOREIGN KEY (payment_id) REFERENCES public.payments_summary_tab(payment_id) NOT VALID;
 N   ALTER TABLE ONLY public.payments_approval_history DROP CONSTRAINT paymant_id;
       public          postgres    false    234    3318    238                       2606    32828    payments_approval payment_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_approval
    ADD CONSTRAINT payment_id FOREIGN KEY (payment_id) REFERENCES public.payments_summary_tab(payment_id) NOT VALID;
 F   ALTER TABLE ONLY public.payments_approval DROP CONSTRAINT payment_id;
       public          postgres    false    238    3318    232                       2606    24747 #   payments_approval_history status_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_approval_history
    ADD CONSTRAINT status_id FOREIGN KEY (status_id) REFERENCES public.payment_agreed_statuses(payment_agreed_status_id) NOT VALID;
 M   ALTER TABLE ONLY public.payments_approval_history DROP CONSTRAINT status_id;
       public          postgres    false    3308    229    234                       2606    24752 !   payments_approval_history user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payments_approval_history
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 K   ALTER TABLE ONLY public.payments_approval_history DROP CONSTRAINT user_id;
       public          postgres    false    234    242    3326                       2606    32853    payment_draft user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.payment_draft
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) NOT VALID;
 ?   ALTER TABLE ONLY public.payment_draft DROP CONSTRAINT user_id;
       public          postgres    false    242    247    3326            �   2   x�3估�b���.v_�taÅ�@V��~.#�s/lU�،U6F��� oI#A      �   G   x�3�0�¾[.쿰�b��rq^X�pa:����_l����2漰��֋�5l	r��qqq �(`      �   ,   x�3�0�¾���]�ra���;��8/,���b#�`� ��      �   3   x�3�4�B##c]s]C#C3+s+SK=#sS3smc�,P)W� �	�      �   -  x���MN�0���)���-�]�ğ�1��c�q$n�I�!#x��W�$~e�B����=yir�&�n�7k��|� \�1'h���+T���A<�!}_Ex����%�(P��O��6$�v�'J�rsMx2g\�x�W���Rj�dR��������t0Dry���z~���w����(�%=������v�T���a͒poV&��(���N��:�p8���9�h2�T��PKZL��-H�%�K�ؗS��~���U�����THR���κ����� ǒ�%��[�����<����      �   �   x���	�P��o��|��9؋�Ĉ�(Tċ$�����0ӑ��o�'x`d7���4�ܹg��;�j��B,��57hXr���V3��0�Ą	O��e�7�:;�-��.����b6���2�� �Ol      �   C   x�3�0����/��,�,�2⼰��9Ӏc��Bf	X�(}���Ƌ�v\إ`����� �UA      �   �   x���=
�@���S�	���������;���� �نH0ƨWxs#g�"J�e�}��̺��8��:É*��c	/p1���s���F(Bb��T)�80��lN���Z�`٪��̲��Sj�cQj��D��Ϝ�Y'���\����r�A�ji�+<d��/Ul�2���������&��T����!�>�����\*2[�����z�QJ=���      �   u  x��U�n�@}^�>&R�JL��A+��16iK+���Vj�6!D�c��`��a��rfl�ZQ����9s;3K[�/�.��r<cw���ϱw�螦�ҍ�Җb�'��\�J��+�	'�Ÿ�9V4�{�ô�6d�hZP��]�?}1�.$Ck�S�.������e����2Č{������*z� ��Д#I��)��"��3&k~��h�p��t�z���� �9!�Ȝhı n8c2<W��(�-g��!�9:'��4*��ڝD���S������]��	�T���D��Ñ�v�)?V� �)x[7liȻ(:��i��jлLİ�ྡྷ	��ְ�Ҋ�9G�d��*�"���=w1pK�G֥��'�f�E� e��<�}-u*�7Hm�!�C�ǍOw�ϡ�uQ��x���;�f9Z�ZRGV��D�e� �(
ٯ�K1l�8-L�Ζ�@ԕ��81�Ņ�e)�^f#�	��h��-)��>F�"�^�FJ�c��$�y����1��S��1�O �Z/8������W�~�m����o/-s��t���&�y�6�|Gqax�ªq���I�pM 3��7>��zV��;�+��J���U�ߴ<�{,�r      �   z   x�m�I
�0е|��K���z�Y
ŋ�2��z��@�<�Z�.Ӻ?kk��Sg�Du���N�LB¢#�� >��~cu�Α�#:��#aU�3)�$^�0�a@2���9��xx����4}      �   k   x�]̱�0���7X
d�qL���� ��#rX῍8��{���{8f��Ҩ'��F���Hm�g��8FcA��]#��N{}�U�s�s�+O�@�6���ʹ^D.�`L�      �   n   x�-��1���J ��m]���:�P��I�e�m֤�8�(�����nۺ����l̅0�xm�'P�c"r�oa�k���b�=�#֋�>���a��>򔯊�N�!      �   T  x�u�ˑ#1C�r�o���
b#���X�=���5.�Y ��J���~Q�"{2��Q�;��!-��K�JU���%u��*�.?�YI��2�����d����j�͜O�E�x��2=����)��bc�vgc�V5������1���P;Q���e*uN%_,��N�jj�beǶ!�&B��^%�J�h���~��2�sxѹ��f }��P�hx|��,����N?���e��>Q�S_���1�^��y�_l���}�K�qlj�`�6���c�%�������������e3��U6��i0�}*NQ^ˡY��
���O|�����Uxvئj+d�[���z9���@η9x,��}��}#�>�@��c0�&=�`(&��
1�5�^�1�b+��W����v0,�ڕ�V�|֨�a��g���Y���1ϐF�X�pLe��mp�iz��c(�>��}ب580�e�v��L�1�u;#��c���6�ڌ$��Z)���=Y�j��uY��~4)�!�ہ>�T�+-k��jw�����������}�~���K	b�{��qZH�w��t��jgS~-���~�����S�      �      x������ � �      �      x������ � �      �   �  x����nE�����UU�N��!�H9$���_�R	B�8�q4NI�W�}����3���x�����{{�W]]�U�2������/�A����0�&���o�QŢ��ϫ��UB���j�����l:�;��
�D���b�����Q�5by���b�%\Pv������M(W��x9L%�*��i���Í8�c�Rz���SZ9ۄ��$P|���ٝxߌ��%�k
KgL���P_B5�&���:�ZMֹs��Ȥ�����3>�4��/�xO4��ʀ_Ɠ� eq��I����Ɗ�i�-Ûb�dѤ<Y�8�":C��w�O2���u�m9����#9Hj��s� 8�n���d�Q��z	v\�tI3�tU�-I�"�\����e�lO%F�4�����q��2d�7
+8�7�dr_��ٷ�?k/��\���̼�S`��ĵ�xmd �l,7�]��ȸ(I��!�CA�`l��e9_�0`nR<��NR��q���InS�RֶZ�����i�*jg�-U�&l�J1�*Ti�#�z��+�'63�S"��`�
Sŀ���&�5�g��"1���v����艔JO�0�	Yf�
�ڮnn߀.��,�='��j
��&�i�OmE����e|u�cA��iHP�3y�>=��`L������^+mV�|p���X��fB`��ğ��O�T0e͚c�<D�z�"G%4�A-���~Pai�qޏ�b��f�ܵ�ʢ�\�sS����_��7x!�|���f�t���agd��d4�=�����������ٝd�Y�c�����n����|���5�q����o�j̞ݙݍ�{�sL|�����4�u�ָ�-+o;��I���������x��3^�����W�sa��]n�$~�����|�jv��㮑��]�8	[R����ى�S0! *-��x�����ט�q=����A5�i�ZM��^C(�Ze5V�~M1���$�8���6�J�x�tC�����/���缳��gc���mn�L�j��z�Й�"w�S��r!�&�g'�����5"�Ԗ7�PSѩ9���ä�
�c��w�㲙@6��tj0��0�½�N$����K<�sd9�(�Sh�AR��7�!��IH�3�����}Ǯ5v�($!�I�"t{�WI�O�?����ξ�u�/�{��d��z ��Z�b�Z��A��\O.�����%.���;&�YB���1%ˠ����`w{������M*U_� �e�3��v�)9�sa��<wNtƩyIC
Lgy���A%{C/�f!/�d��JT���b�X6"�4!1�����a���'.���40,D,���QE`��J�˅�r������7]�C�VW�Y���#�sQ[��#��Ͼ������Z�N�4�oMm���:X� _k����Oo�      �   G   x�3�LL����4�2�L�,JM.�/�4�2��I,�L-�4�2�,-2��9SRJ�3RS8��b���� P�      �   d  x����jA��=O���$C�Su�N��5�$F2���ԕ4s1�2�[�\��@B$�3t��j�D�0�Mw5�����C{�~i\}�?۳��������B�rU�U�+@��Z�E��w���:�㘱>>pH�֢{�OF����tN�P?x��(�S0.� A��i�,��J!��H2�� ����v>t�(h���=]�����%�y{q���^�&�6��L
��z�X�F�A�&F�A�b��-}�==~3�9:����.��e�Q����cɞ<{
&f�������堛����]K��(�
��h����=twwp�ַ(����dmKT�!c��V
J)Z�NyCB"r�YdfR�Â����t��}`-����7�ۧ�[�`���zԏ �t�S�Kl
9�S2Cy�21F��␭ �>�dPyD)D��T�~����Ҙ�%��_���I�5�ѿE?�Z���,�39i^�9�x5�>�9�f*�ڢ7>���Ҏ<٬}R"Je�Q���)"�2���� n��ޠV k�`���ҫ-o63=�����F����-a�	�<Z�T��Q]pG�Ke�^��冄�&A�ٱfa���^�M�g�      �   $   x�3�بpa�)rq^�xa��0~� ��     