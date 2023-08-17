columns = ('balance_sum', 'company_id', '222')
expr_set = ', '.join([f"{col} = c.{col}" for col in columns[:-1]])
print(expr_set)
