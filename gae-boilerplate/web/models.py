from google.appengine.ext import ndb

class ProfileData(ndb.Model):
	source=ndb.StringProperty()
	identificador=ndb.StringProperty()
	name=ndb.StringProperty()
	location=ndb.StringProperty()
	current_company=ndb.StringProperty()
	current_company_investors=ndb.StringProperty(repeated=True)
	prior_company=ndb.StringProperty(repeated=True)
	past_companies=ndb.StringProperty(repeated=True)
	tweeter_profile=ndb.StringProperty()
	photo=ndb.StringProperty(repeated=True)
	jsonUserData=ndb.TextProperty()
	jsonStartupsData=ndb.TextProperty()
	startups_ids=ndb.TextProperty()
	startups_nombres=ndb.TextProperty()

class Company(ndb.Model):
	source=ndb.StringProperty()
	identificador=ndb.StringProperty()
	name=ndb.StringProperty()
	investors=ndb.TextProperty()

class Groups(ndb.Model):
	name=ndb.StringProperty()
	companies=ndb.StringProperty()