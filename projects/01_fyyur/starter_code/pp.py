@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    new_venue = Venue()
    form_data = VenueForm(request.form)
    form_data.populate_obj(new_venue)
    db.session.add(new_venue)
    db.session.commit()
  except:
      error = True
      db.session.rollback()
  finally:
      db.session.close()
      if not error : 
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
      else:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was not listed! An error occured')

      # DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      return render_template('pages/home.html')
"""