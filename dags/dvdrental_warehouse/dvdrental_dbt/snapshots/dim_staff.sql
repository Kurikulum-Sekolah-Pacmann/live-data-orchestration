{% snapshot dim_staff %}

{{
    config(
      target_database='warehouse',
      target_schema='warehouse',
      unique_key='sk_staff_id',

      strategy='check',
      check_cols=[
			'first_name',
			'last_name',
			'address',
			'email',
			'active',
			'username',
			'password',
			'district',
			'phone',
			'city',
			'country' 
		]
    )
}}

with stg__staff as (
	select *
	from {{ source("staging", "staff") }}
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

dim_staff as (
	select 
		ss.staff_id as nk_staff_id,
		ss.first_name,
		ss.last_name,
		sa.address,
		ss.email,
		ss.active,
		ss.username,
		ss."password",
		sa.district,
		sa.phone,
		sc.city,
		sc2.country 
	from stg__staff ss 
	join stg__address sa 
		on sa.address_id = ss.address_id 
	join stg__city sc 
		on sc.city_id = sa.city_id 
	join stg__country sc2 
		on sc2.country_id = sc.country_id
),

final_dim_staff as (
	select
		nk_staff_id as sk_staff_id, 
		* 
	from dim_staff
)

select * from final_dim_staff

{% endsnapshot %}