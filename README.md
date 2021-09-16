# InterestApp-API
Simple Flask-SQLAlchemy app to practice.

CRUD for saving compound interest investments.

'/' to query all rows (GET)

'/insert' to insert new row (POST)

'/delete/<int:id>' to delete a row (DELETE)

'/edit/<int:id>' to edit a row (PUT)

Each row receives 'name', 'initial_capital', 'rate', 'effective_rate', 'number_of_periods' and 'final_sum'. Planning to add 'effective_rate' and 'final_sum' calculations so
that those two fields dont have to be sent from the frontend.
