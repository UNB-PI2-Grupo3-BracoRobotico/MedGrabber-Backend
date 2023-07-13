from datetime import datetime
import logging
from collections import defaultdict
import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from grabber_backend.database_controller.models import (
    Base,
    User,
    Product,
    DatabaseOrder,
    OrderProduct,
    Payment,
    Position,
    UserRoleEnum,
    OrderStatusEnum,
    PaymentStatusEnum,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OrderDatabaseHandler:
    def __init__(self, session):
        self.session = session

    # Call the stored procedure to create an order
    def create_order(self, order: DatabaseOrder):
        from pprint import pprint

        pprint(order)
        result = self.session.execute(
            text(
                "SELECT insert_new_order(:user_id, :order_date, :total_cost, :order_status)"
            ),
            {
                "user_id": order.user,
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_cost": order.total_price,
                "order_status": order.order_status,
            },
        )

        order_id = result.fetchone()[0]

        self.session.commit()

        pprint(f"ID DO PEDIDO: {order_id}")

        for product in order.order_items:
            logger.info(product)
            self.session.execute(
                text(
                    """
                    CALL insert_order_product_and_update_position(:order_id, :product_id, :product_amount, :user_id);
                    """
                ),
                {
                    "product_id": product["product_id"],
                    "product_amount": product["amount"],
                    "order_id": order_id,
                    "user_id": order.user,
                },
            )

        self.session.commit()

        return order_id

    def get_orders(self):
        result = self.session.execute(
            text(
                """
            SELECT
                co.customer_order_id,
                co.user_id,
                u.email,
                co.order_date,
                co.total_cost,
                co.order_status,
                op.product_id,
                p.product_name,
                p.product_description,
                p.product_price,
                op.product_amount,
                pos.position_x,
                pos.position_y
            FROM
                customer_order co
            JOIN 
                users u ON co.user_id = u.user_id
            JOIN 
                order_product op ON co.customer_order_id = op.customer_order_id
            JOIN 
                product p ON op.product_id = p.product_id
            JOIN
                position pos ON p.product_id = pos.product_id;
        """
            )
        )
        rows = result.fetchall()

        orders_dict = defaultdict(lambda: defaultdict(set))
        for row in rows:
            order_id = row[0]
            orders_dict[order_id]["user_id"].add(row[1])
            orders_dict[order_id]["email"].add(row[2])
            orders_dict[order_id]["order_date"].add(row[3])
            orders_dict[order_id]["total_cost"].add(row[4])
            orders_dict[order_id]["order_status"].add(row[5])
            product = {
                "product_id": row[6],
                "product_name": row[7],
                "product_description": row[8],
                "product_price": float(row[9]),
                "product_amount": row[10],
                "position_x": row[11],
                "position_y": row[12],
            }
            orders_dict[order_id]["products"].add(json.dumps(product))

        orders = []
        for order_id, order_data in orders_dict.items():
            order = {
                "customer_order_id": order_id,
                "user_id": list(order_data["user_id"])[0],
                "email": list(order_data["email"])[0],
                "order_date": list(order_data["order_date"])[0],
                "total_cost": float(list(order_data["total_cost"])[0]),
                "order_status": list(order_data["order_status"])[0],
                "products": [json.loads(prod) for prod in order_data["products"]],
            }
            orders.append(order)

        return orders
