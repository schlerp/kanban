import datetime

from app import db, models


def create_status():
    '''creates the three main stati'''
    todo = models.Status('todo')
    doing = models.Status('doing')
    done = models.Status('done')
    
    db.session.add(todo)
    db.session.add(doing)
    db.session.add(done)
    db.session.commit()


def create_tasks():
    '''create some sample tasks'''
    #task1 = models.Task(title='Create App',
                        #description='Create the main skeleton of the application, this iwll be a proof of concept prototype',
                        #creator="patty",
                        #creation_date=datetime.datetime.utcnow(),
                        #owner="other person",
                        #owned_date=datetime.datetime.utcnow(),
                        #status=models.Status.query.filter_by(name='todo').first())
    
    #task2 = models.Task(title='Build HTML Templates',
                        #description='Create the HTML Templates to be used in this application',
                        #creator="patty",
                        #creation_date=datetime.datetime.utcnow(),
                        #owner=None,
                        #owned_date=None,
                        #status=models.Status.query.filter_by(name='doing').first())
    
    #task3 = models.Task(title='Consistently style application',
                        #description='Create a onsistant style sheet for this application',
                        #creator="patty",
                        #creation_date=datetime.datetime.utcnow(),
                        #owner="patty",
                        #owned_date=datetime.datetime.utcnow(),
                        #status=models.Status.query.filter_by(name='done').first())
    task4 = models.Task(title='Implement project scoping',
                        description='Implement and test project scoping, this is left out of a particular project scope and should therefore only appear in the global view',
                        creator='derp',
                        creation_date=datetime.datetime.utcnow(),
                        status=models.Status.query.filter_by(name='todo').first())
    
    db.session.add(task4)
    db.session.commit()

def create_user():
    '''creates a test user'''
    user1 = models.User("derp", "herp")
    db.session.add(user1)
    db.session.commit()

if __name__ == '__main__':
    create_tasks()