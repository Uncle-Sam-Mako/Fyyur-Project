
def searchFunction(table, search_term):
  results = table.query.filter(table.name.ilike(f"%{search_term}%"))
  response={
    "count": results.count(),
    "data": results
  }
  return response