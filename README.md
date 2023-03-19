# social-video-django-server
This Django project provexcu robust API for a premium content sharing platform. On this platform, creators would create content that could be free or premium for 'regular' users.  The API is documented at https://bit.ly/3X7GaUX

The project's django config folder is named djangoserver. I know it isn't structured exactly pleasantly, my apologies 🙃

To test run it, make sure you've got Docker and Docker-compose installed.

Build up and start the containers that make up the project. On Linux, you'd do something like:

  docker-compose up --build

to start and:

  docker-compose down

in another terminal window to kill it.

Finally, to fully test the API, you'll need to be able to do two things that aren't accessible via the API:

	1. Verify creator accounts. Creators need to be verified before they are allowed to upload content and enjoy other creator privileges.
	2. Deposit money into users' wallets. This is meant to be temporary till the code integrates with a payment gateway.
	
	These two actions have to be completed by a staff user.
	
There has to be a superuser that can create new staff accounts and has unrestricted access to users data. To create this account, while the server is running, run this in another terminal window (in the root folder of the code):

 	docker-compose exec server python manage.py createsuperuser

There will be prompts to create the superuser account.

You can now access the admin panel at localhost:8000/admin/

This is what verifying a creator account looks like

![Screenshot from 2023-01-13 09-48-33](https://user-images.githubusercontent.com/70032662/212278479-c2480e30-8585-4f74-adda-f16d83a70263.png)

And this is what depositing money into a user's account looks like

![Screenshot from 2023-01-13 09-48-55](https://user-images.githubusercontent.com/70032662/212278629-80052e37-4247-49d6-a56d-e2ee471f4209.png)

And of course, don't forget to read the doc at https://bit.ly/3X7GaUX :)
