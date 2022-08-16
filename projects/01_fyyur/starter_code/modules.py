import re

def searchFunction(table, search_term):
  results = table.query.filter(table.name.ilike(f"%{search_term}%"))
  response={
    "count": results.count(),
    "data": results
  }
  return response

def formatGenre(data):
  genres = re.findall('\{(.*?)\}',data.genres)
  data.genres = genres[0].split(",")