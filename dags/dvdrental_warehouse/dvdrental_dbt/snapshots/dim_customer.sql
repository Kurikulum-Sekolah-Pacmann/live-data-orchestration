{% snapshot dim_customer %}

{{
    config(
      target_database='warehouse',
      target_schema='warehouse',
      unique_key='sk_customer_id',

      strategy='check',
      check_cols=[
			'first_name',
			'last_name',
			'email',
			'phone',
			'postal_code',
			'address',
			'city',
			'district',
			'country',
			'activebool',
			'active'
		]
    )
}}

with stg__customer as (
	select *
	from {{ source("staging", "customer") }}
),

stg__address as (
	select *
	from {{ source("staging", "address") }} 
),

stg__city as (
	select *
	from {{ source("staging", "city") }}  
),

stg__country as (
	select *
	from {{ source("staging", "country") }}
),

dim_customer as (
	select 
		sc.customer_id as nk_customer_id,
		sc.first_name,
		sc.last_name,
		sc.email,
		sa.phone,
		sa.postal_code,
		sa.address,
		sc2.city,
		sa.district,
		sc3.country,
		sc.activebool,
		sc.active
	from stg__customer sc 
	join stg__address sa 
		on sa.address_id = sc.address_id 
	join stg__city sc2 
		on sc2.city_id = sa.city_id 
	join stg__country sc3 
		on sc3.country_id = sc2.country_id 
),

final_dim_customer as (
	select
		nk_customer_id as sk_customer_id, 
		* 
	from dim_customer
)

select * from final_dim_customer

{% endsnapshot %}