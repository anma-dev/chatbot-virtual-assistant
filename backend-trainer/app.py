from aiohttp import web
import socketio
from models import DbName, ProjectsModel, DomainsModel, IntentsModel, ResponseModel, StoryModel, EntityModel, RefreshDb, StoryDetail

# creates a new Async Socket IO Server

sio = socketio.AsyncServer(logger=True, engineio_logger=True)

''' Creates a new Aiohttp Web Application '''

app = web.Application()

# Binds our Socket.IO server to our Web App
# instance

sio.attach(app)

# we can define aiohttp endpoints just as we normally
# would with no change


async def index(request):
    print(request)
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


''' Events handlers for connect and disconnect , nothing special is done except logging'''


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    print('Environment ', environ)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


''' Events handlers for Join room and leave room , 
This method contains join room and leave room for all name spaces. This was introduced to ensure join room and leave 
room happens within the namespace'''


@sio.on('join_room', namespace='/project')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /project_______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/project')
    sio.enter_room(sid, room=sid, namespace='/project')


@sio.on('leave_room', namespace='/project')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /project_______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/project')
    sio.leave_room(sid, room=sid, namespace='/project')


@sio.on('join_room', namespace='/domain')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /domain _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/domain')
    sio.enter_room(sid, room=sid, namespace='/domain')


@sio.on('leave_room', namespace='/domain')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /domain _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/domain')
    sio.leave_room(sid, room=sid, namespace='/domain')


@sio.on('join_room', namespace='/intent')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /intent _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/intent')
    sio.enter_room(sid, room=sid, namespace='/intent')


@sio.on('leave_room', namespace='/intent')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /intent _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/intent')
    sio.leave_room(sid, room=sid, namespace='/intent')


@sio.on('join_room', namespace='/response')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /response _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/response')
    sio.enter_room(sid, room=sid, namespace='/response')


@sio.on('leave_room', namespace='/response')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /response _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/response')
    sio.leave_room(sid, room=sid, namespace='/response')


@sio.on('join_room', namespace='/story')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /story _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/story')
    sio.enter_room(sid, room=sid, namespace='/story')


@sio.on('leave_room', namespace='/story')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /story _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/story')
    sio.leave_room(sid, room=sid, namespace='/story')


@sio.on('join_room', namespace='/dashboard')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /dashboard _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/dashboard')
    sio.enter_room(sid, room=sid, namespace='/dashboard')


@sio.on('leave_room', namespace='/dashboard')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /dashboard _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/dashboard')
    sio.leave_room(sid, room=sid, namespace='/dashboard')


@sio.on('join_room', namespace='/nav')
async def join_room(sid, room_name):
    print("________________________ User {} joined room {} with namespace /dashboard _______________________".format(sid, room_name))
    sio.enter_room(sid, room=room_name, namespace='/nav')
    sio.enter_room(sid, room=sid, namespace='/nav')


@sio.on('leave_room', namespace='/nav')
async def leave_room(sid, room_name):
    print("________________________ User {} Left room {} with namespace /dashboard _______________________".format(sid, room_name))
    sio.leave_room(sid, room=room_name, namespace='/nav')
    sio.leave_room(sid, room=sid, namespace='/nav')


''' Refresh seed data. 

This method will wip off the mongo db instance of all user created data and reload it with seed data. 
This endpoint needs to be used with caution and ensure proper backup is taken before this is invoked '''


@sio.on('refresh_data', namespace='/refresh')
async def refresh_data(sid):
    print("##################################User {} Requested to refresh DB  ##########################".format(sid))

    result = await RefreshDb.refreshdb()
    await sio.emit('refresh', result)


'''Projects Endpoints 

These contains methods to get all projects , update delete and insert new project in the mongo db'''

ProjectsModel = ProjectsModel()


@sio.on('getProjects', namespace='/project')
async def get_projects(sid, room_name):

    print("---------- Request from Session {} -------------- ".format(sid))

    result = await ProjectsModel.get_projects()
    await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('createProject', namespace='/project')
async def create_projects(sid, record, room_name):

    print("---------- Request from Session {} -- with record {} ------------ ".format(sid, record))

    message = await ProjectsModel.create_projects(record)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('copyProject', namespace='/project')
async def copy_projects(sid, record, room_name):

    print("---------- Request from Session {} -- with record {} ------------ ".format(sid, record))

    message = await ProjectsModel.copy_project(record)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('deleteProject', namespace='/project')
async def delete_project(sid, object_id, room_name):

    print("---------- Request from Session {} --- with record {} ----------- ".format(sid, object_id))

    message = await ProjectsModel.delete_project(object_id)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    result = await ProjectsModel.get_projects()
    await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('updateProject', namespace='/project')
async def update_project(sid, update_query, room_name):

    print("---------- Request from Session {} - with record {} ------- ".format(sid, update_query))

    message = await ProjectsModel.update_project(update_query)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)


# Domains Endpoints

DomainsModel = DomainsModel()


@sio.on('getDomains', namespace='/domain')
async def get_domains(sid, project_id, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, project_id, room_name))

    result = await DomainsModel.get_domains(project_id)
    await sio.emit('allDomains', result, namespace='/domain', room=room_name)


@sio.on('createDomain', namespace='/domain')
async def create_domain(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.create_domain(data)
    await sio.emit('domainResponse', message, namespace='/domain', room=sid)

    if domains_list is not None:
        await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


@sio.on('deleteDomain', namespace='/domain')
async def delete_domain(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.delete_domain(data)

    await sio.emit('domainResponse', message, namespace='/domain', room=sid)
    await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


@sio.on('updateDomain', namespace='/domain')
async def update_domains(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.update_domain(data)
    print("Message value {}".format(message))
    await sio.emit('domainResponse', message, room=sid, namespace='/domain')

    if domains_list is not None:
        await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


# intents Endpoint
IntentsModel = IntentsModel()


@sio.on('getIntents', namespace='/dashboard')
async def get_intents(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    intents_list = await IntentsModel.get_intents(data)
    await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('createIntent', namespace='/dashboard')
async def create_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.create_intent(data)
    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)

    if intents_list is not None:
        await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('deleteIntent', namespace='/dashboard')
async def delete_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.delete_intent(data)

    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('updateIntent', namespace='/dashboard')
async def update_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.update_intent(data)
    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)

    if intents_list is not None:
        await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('intentDetails', namespace='/intent')
async def get_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    intent_detail = await IntentsModel.get_intent_details(data)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


@sio.on('modifyIntentDetails', namespace='/intent')
async def insert_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await IntentsModel.modify_intent_detail(data)
    await sio.emit('responseDetail', message, namespace='/intent', room=sid)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


@sio.on('deleteIntentDetails', namespace='/intent')
async def insert_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await IntentsModel.delete_intent_detail(data)
    await sio.emit('responseDetail', message, namespace='/intent', room=sid)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)



# responses Endpoints
ResponseModel = ResponseModel()


@sio.on('getResponses', namespace='/dashboard')
async def get_responses(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    responses_list = await ResponseModel.get_responses(data)
    await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('createResponse', namespace='/dashboard')
async def create_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.create_response(data)

    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)

    if responses_list is not None:
        await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('deleteResponse', namespace='/dashboard')
async def delete_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.delete_response(data)

    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('updateResponse', namespace='/dashboard')
async def update_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.update_response(data)
    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)

    if responses_list is not None:
        await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


# Endpoints for Stories
StoryModel = StoryModel()


@sio.on('getStories', namespace='/dashboard')
async def get_stories(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    stories_list = await StoryModel.get_stories(data)
    await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('createStory', namespace='/dashboard')
async def create_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.create_story(data)
    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)

    if stories_list is not None:
        await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('deleteStory', namespace='/dashboard')
async def delete_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.delete_story(data)

    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('updateStory', namespace='/dashboard')
async def update_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.update_story(data)

    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)

    if stories_list is not None:
        await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


# Entities Endpoints

EntityModel = EntityModel()


@sio.on('getEntities', namespace='/nav')
async def get_entities(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    entities_list = await EntityModel.get_entities(data)
    await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('createEntity', namespace='/nav')
async def create_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    message, entities_list = await EntityModel.create_entity(data)
    await sio.emit('entitiesResponse', message, namespace='/nav', room=room_name)

    if entities_list is not None:
        await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('deleteEntity', namespace='/nav')
async def delete_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, entities_list = await EntityModel.delete_entity(data)

    await sio.emit('entitiesResponse', message, namespace='/nav', room=sid)
    await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('updateEntity', namespace='/nav')
async def update_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    message, entities_list = await EntityModel.update_entity(data)
    await sio.emit('entitiesResponse', message, namespace='/nav', room=room_name)

    if entities_list is not None:
        await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


# get Stories Details endpoints

StoryDetail = StoryDetail()


@sio.on('getStoryDetails', namespace='/story')
async def getstoriesdetail(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    story_details = await StoryDetail.getstorydetail(data)

    await sio.emit('storyDetails', story_details, namespace='/story', room=room_name)


# We bind our aiohttp endpoint to our app


app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    sio.attach(app)
    web.run_app(app, port=8089)
