from init import *
from config import *
from modules import *
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  areas = []
  for venue in venues:
    area = {
      "city" : venue.city,
      "state" : venue.state,
      "venues" : Venue.query.filter(and_(Venue.city == venue.city, Venue.state == venue.state)).order_by(Venue.id).all()
    }
    areas.append(area)
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  return render_template('pages/search_venues.html', results=searchFunction(Venue, search_term), search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  venue_info = Venue.query.get(venue_id)
  upcoming = db.session.query(Venue, Show).join(Show).filter(Venue.id == venue_id, Show.start_time > datetime.now()) #Query for getting all the venue's upcoming shows
  past_shows = db.session.query(Venue, Show).join(Show).filter(Venue.id == venue_id, Show.start_time <= datetime.now())#Query for getting all the venue's past shows
  venue_info.upcoming_shows = []
  venue_info.past_shows = []
  for venue, show in upcoming.all():
    artist = {
      'artist_image_link' : Artist.query.get(show.artist_id).image_link,
      'artist_name' : Artist.query.get(show.artist_id).name,
      'artist_id' : show.artist_id,
      'start_time' : show.start_time,
    }
    venue_info.upcoming_shows.append(artist)

  for venue, show in past_shows.all():
    artist = {
      'artist_image_link' : Artist.query.get(show.artist_id).image_link,
      'artist_name' : Artist.query.get(show.artist_id).name,
      'artist_id' : show.artist_id,
      'start_time' : show.start_time,
    }
    venue_info.past_shows.append(artist)
  venue_info.upcoming_shows_count = upcoming.count()
  venue_info.past_shows_count = past_shows.count()
  venue_info.website = venue_info.website_link
  formatGenre(venue_info)
  return render_template('pages/show_venue.html', venue=venue_info)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(request.form)
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  form_data = VenueForm(request.form)
  if form_data.validate():
    try:
        new_venue = Venue()
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
          # on unsuccessful db insert, flash error
          flash('Venue ' + request.form['name'] + ' was not listed! An error occured', 'error')

        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')
  for error in form_data.errors:
    flash(form_data.errors[error][0], 'error') 
  return render_template('forms/new_venue.html', form=form_data)

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  selectedVenue = Venue.query.get(venue_id)
  error = False
  try:
    deleted = request.get_json()['deleted']
    show_to_delete = Show.query.filter(Show.venue_id == venue_id).all()
    artist_venue_records = Show.query.filter(artist_venue.venue_id == venue_id).all()
    venue = Venue.query.get(venue_id)
    if deleted :
      db.session.delete(venue) 
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
    if not error : 
      # on successful db update, flash success
      flash('Venue ' + selectedVenue['name'] + ' was successfully deleted!')
    else:
      # on successful db update, flash success
      flash('Venue ' + selectedVenue['name'] + ' was not deleted! An error occured', 'error')
  return redirect(url_for('home'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  #DONE: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  return render_template('pages/search_artists.html', results=searchFunction(Artist, search_term), search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id
  artist_info = Artist.query.get(artist_id)
  upcoming = db.session.query(Artist, Show).join(Show).filter(Artist.id == artist_id, Show.start_time > datetime.now()) #Query for getting all the artist's upcoming shows
  past_shows = db.session.query(Artist, Show).join(Show).filter(Artist.id == artist_id, Show.start_time <= datetime.now())#Query for getting all the artist's past shows
  artist_info.upcoming_shows = []
  artist_info.past_shows = []

  for artist, show in upcoming.all():
    venue = {
      'venue_image_link' : Venue.query.get(show.venue_id).image_link,
      'venue_name' : Venue.query.get(show.venue_id).name,
      'venue_id' : show.venue_id,
      'start_time' : show.start_time,
    }
    artist_info.upcoming_shows.append(venue)

  for artist, show in past_shows.all():
    venue = {
      'venue_image_link' : Venue.query.get(show.venue_id).image_link,
      'venue_name' : Venue.query.get(show.venue_id).name,
      'venue_id' : show.venue_id,
      'start_time' : show.start_time,
    }
    artist_info.past_shows.append(venue)


  artist_info.upcoming_shows_count = upcoming.count()
  artist_info.past_shows_count = past_shows.count()
  artist_info.website = artist_info.website_link
  formatGenre(artist_info)
  return render_template('pages/show_artist.html', artist=artist_info)

#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)
  selectedArtist = Artist.query.get(artist_id)
  if request.method == 'POST':
    error = False
    if(form.validate()):
      try:
        form.populate_obj(selectedArtist)
        db.session.commit()
        formatGenre(selectedArtist)
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()
        if not error : 
          # on successful db update, flash success
          flash('Artist ' + request.form['name'] + ' was successfully edited!')
        else:
          # on successful db update, flash success
          flash('Artist ' + request.form['name'] + ' was not edited! An error occured', 'error')
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
      for error in form.errors:
        flash(form.errors[error][0], 'error') 
      return render_template('forms/edit_artist.html', form=form, artist=selectedArtist)

  # DONE: populate form with fields from artist with ID <artist_id>
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form.name.data = selectedArtist.name
  form.phone.data = selectedArtist.phone
  form.genres.data = selectedArtist.genres
  form.city.data = selectedArtist.city
  form.state.data = selectedArtist.state
  form.facebook_link.data = selectedArtist.facebook_link
  form.image_link.data = selectedArtist.image_link
  form.website_link.data = selectedArtist.website_link
  form.seeking_description.data = selectedArtist.seeking_description
  form.seeking_venue.data = selectedArtist.seeking_venue
  return render_template('forms/edit_artist.html', form=form, artist=selectedArtist)
 
@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  selectedVenue = Venue.query.get(venue_id)
  if request.method == 'POST':
      error = False
      if(form.validate()):
        try:
            form.populate_obj(selectedVenue)
            db.session.commit()
            formatGenre(selectedVenue)
        except:
            error = True
            db.session.rollback()
        finally:
          db.session.close()
          if not error : 
            # on successful db update, flash success
            flash('Venue ' + request.form['name'] + ' was successfully edited!')
          else:
            # on unsuccessful db update, flash error
            flash('Venue ' + request.form['name'] + ' was not edited! An error occured', 'error')
          return redirect(url_for('show_venue', venue_id=venue_id))
      else:
        for error in form.errors:
          flash(form.errors[error][0], 'error') 
        return render_template('forms/edit_venue.html', form=form, venue=selectedVenue)
  
  # DONE: populate form with fields from venue with ID <venue_id>
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form.name.data = selectedVenue.name
  form.phone.data = selectedVenue.phone
  form.genres.data = selectedVenue.genres
  form.city.data = selectedVenue.city
  form.address.data = selectedVenue.address
  form.state.data = selectedVenue.state
  form.facebook_link.data = selectedVenue.facebook_link
  form.image_link.data = selectedVenue.image_link
  form.website_link.data = selectedVenue.website_link
  form.seeking_description.data = selectedVenue.seeking_description
  form.seeking_talent.data = selectedVenue.seeking_talent
  return render_template('forms/edit_venue.html', form=form, venue=selectedVenue)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(request.form)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  form_data = ArtistForm(request.form)
  if form_data.validate():
    try:
      new_artist = Artist()
      form_data.populate_obj(new_artist)
      db.session.add(new_artist)
      db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if not error : 
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
        else:
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was not listed! An error occured', 'error')

        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')
  for error in form_data.errors:
    flash(form_data.errors[error][0], 'error') 
  return render_template('forms/new_artist.html', form=form_data)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  shows = []
  for show in Show.query.all():
    info = {
      'artist_id': show.artist_id,
      'venue_id' : show.venue_id,
      'artist_name' : Artist.query.get(show.artist_id).name,
      'artist_image_link' : Artist.query.get(show.artist_id).image_link,
      'venue_name' : Venue.query.get(show.venue_id).name
    }
    shows.append(info)
  return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    new_Show = Show()
    form_data = ShowForm(request.form)
    if form_data.validate():
      form_data.populate_obj(new_Show)
      venue = Venue.query.get(form_data.venue_id.data)
      artist = Artist.query.get(form_data.artist_id.data)
      venue.artists.append(artist) #Add Artist & Venue to artist_venue
      db.session.add(new_Show)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if not error : 
        # on successful db insert, flash success
        flash('Show  was successfully listed!')
      else:
        # on successful db insert, flash success
        if(artist and venue):
          flash('Show was not listed! An error occured')
        else:
          flash('The artist or the venue does not exist in the database :(')

      # DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show ' + data.name + ' could not be listed.')
      return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
