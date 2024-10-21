{% snapshot dim_store %}

{{
    config(
      target_database='warehouse',
      target_schema='warehouse',
      unique_key='sk_store_id',

      strategy='check',
      check_cols=[
			'address',
			'district',
			'city',
			'country' 
		]
    )
}}

with stg__store as (
	select *
	from {{ source("staging", "store") }}
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

dim_store as (
	select 
		ss.store_id as nk_store_id,
		sa.address,
		sa.district,
		sc.city,
		sc2.country 
	from stg__store ss
	join stg__address sa 
		on sa.address_id = ss.address_id 
	join stg__city sc 
		on sc.city_id = sa.city_id 
	join stg__country sc2 
		on sc2.country_id = sc.country_id 
),

final_dim_store as (
	select
		nk_store_id as sk_store_id, 
		* 
	from dim_store
)

select * from final_dim_store

{% endsnapshot %}