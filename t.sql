with items as (
                      select item_id, category
                      from (
                       select item_id, category, cnt,
                              rank() over (partition by category order by cnt desc) mrank
                       from (
                        select item_id, category, count(1) as cnt
                        from orders a join order_details b
                         on a.order_id = b.order_id and a.order_date >= now() - interval '1' day
                        group by item_id, category
                        ) t
                       ) t where mrank <= 5 order by cnt desc
                      )
                      SELECT id,name,price, description,img_url,'apparels' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM apparels a join items i on i.item_id = a.id and i.category='apparels'
                       left outer join reviews r on r.category='apparels' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name,price, description,img_url,'fashion' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM fashion a join items i on i.item_id = a.id and i.category='fashion'
                       left outer join reviews r on r.category='fashion' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'bicycles' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM bicycles a join items i on i.item_id = a.id and i.category='bicycles'
                       left outer join reviews r on r.category='bicycles' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'jewelry' as category, count(1) review_cnt, round(avg(rating)*20) rating
                       FROM jewelry a join items i on i.item_id = a.id and i.category='jewelry'
                       left outer join reviews r on r.category='jewelry' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url;

