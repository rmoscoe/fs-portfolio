# Portfolio

## Table of Contents

- [Portfolio](#portfolio)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Technology Used](#technology-used)
    - [Badges](#badges)
  - [Code Examples](#code-examples)
  - [Installation and Usage](#installation-and-usage)
    - [Installation](#installation)
    - [Usage](#usage)
  - [Lessons Learned](#lessons-learned)
  - [Author Info](#author-info)
    - [Ryan Moscoe](#ryan-moscoe)
  - [Future Development](#future-development)
  - [License](#license)
  - [Contributing](#contributing)

<br/>

## Description 

[Visit the Deployed Site](https://www.ryanmoscoe.com/)

I built this responsive website as a portfolio to showcase my work. The projects in my portfolio demonstrate my skill with a variety of technologies, as well as my evolution as a developer. The portfolio itself also serves as an example of my skill with Python, Django, MySQL, TailwindCSS, and Alpine.js. This site looks similar to my previous (legacy) portfolio, but it has been refactored to include a back end so it can support a blog. I've also made some improvements to the UI, particularly on small screens.

<br/>

![Homepage with photo of a man and white text against a dark gray background](/client/static_src/src/images/fs_portfolio.jpg)

<br/>

## Technology Used 

| Technology Used         | Resource URL           | Purpose |
| :------------- |:-------------:| :---------- |
| HTML    | [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) | Page structure |
| CSS     | [https://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)      |   Page styling and positioning of elements |
| TailwindCSS | [https://tailwindcss.com/](https://tailwindcss.com/) | Utility-first CSS framework |
| JavaScript | [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | Page interactivity and logic |
| Alpine.js | [https://www.alpinejs.dev/](https://www.alpinejs.dev/) | Lightweight JavaScript framework for scripting and reactivity within markup |
| Python | [https://www.python.org/](https://www.python.org/) | Backend logic |
| Django | [https://www.djangoproject.com/](https://www.djangoproject.com/) | Full-stack web development framework, including Object Relational Model (ORM), server, and template engine |
| MySQL | [https://www.mysql.com/](https://www.mysql.com/) | Relational database (production) |
| SQLite | [https://sqlite.org/](https://sqlite.org/) | Relational database (development) |
| Twilio | [https://www.twilio.com/en-us](https://www.twilio.com/en-us) | SMS Messaging for two-factor authentication |
| Zoho | [https://www.zoho.com/](https://www.zoho.com/) | Email hosting |
| Cloudflare | [https://www.cloudflare.com/](https://www.cloudflare.com/) | Domain registration |
| Amazon Web Services (AWS) | [https://aws.amazon.com/](https://aws.amazon.com/) | S3 storage for uploads |
| Heroku | [https://www.heroku.com/](https://www.heroku.com/) | Hosting; Platform as a Service (PaaS) |
| Git | [https://git-scm.com/](https://git-scm.com/)  |  Version control |

<br/>

### Badges

![Static Badge](https://img.shields.io/badge/Python-52.1%25-%23437CAB) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/HTML-41.2%25-%23e34c26) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/CSS-6.5%25-%23264de4) &nbsp; &nbsp; ![Static Badge](https://img.shields.io/badge/JavaScript-0.1%25-%23f0db4f)

<br/>

## Code Examples

I wanted to sequence the projects in my portfolio with the most impactful projects first. However, I didn't want to hard-code the projects in a particular order, becase 1) I wanted to allow for flexibility as I create new projects or update existing ones, and 2) I wanted to allow visitors to sort and filter the projects. It seemed reasonable to me that a recruiter or hiring manager might want to filter for a particular skill or sort the projects in a different order--and since I haven't seen that functionality in many portfolios, I felt adding it could give me a leg up on the competition.

To meet these requirements, I created database models for my projects and added a `show_after` field using a `OneToOneField`. This allowed me to build a sort function based on the idea of a linked list without actually implementing a linked list and locking the order of the projects. Here is that sort function:


```python
def sort_as_linked_list(iterable):
    sorted_list = []
    next_item_map = {}
    current = None
    for obj in iterable:
        if obj.show_after is None or obj.show_after not in list(iterable):
            current = obj
        else:
            next_item_map[obj.show_after.id] = obj
    while current is not None:
        sorted_list.append(current)
        current = next_item_map.get(current.id)
    return sorted_list
```

On the front end, I implemented sort and filter functionality using Alpine.js. For filtering, I used an `x-data` attribute to hold a list of values for each filter, along with `$dispatch` to dispatch an event when the filter values change. Each project element listens for that event with an `@filter-change.window` attribute and shows or hides itself according to the filter values. For sorting, I added a method to an `x-data` attribute on the project's container element, along with an `x-init` attribute using a `$watch` function to invoke the sorting method whenever the sort value changes:


```html
<div
    class="bg-stealth-800 mb-3 flex flex-wrap sm:flex-nowrap w-full justify-around items-center gap-x-3 gap-y-2 md:gap-x-4 lg:gap-x-6 py-2 md:py-4"
    x-data="{
        sortProjects: (sortBy) => {
            if (sortBy === 'A-Z') {
                projects.sort((a, b) => a.name.localeCompare(b.name));
            } else if (sortBy === 'Z-A') {
                projects.sort((a, b) => b.name.localeCompare(a.name));
            } else if (sortBy === 'Newest') {
                projects.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            } else {
                JSON.parse({{ projects|json_helper:'dumps' }})
            }
        }
    }"
    x-init="$watch('sort', value => sortProjects(value))"
>
    ...
</div>
```

<br/>

## Installation and Usage 

### Installation

As a visitor, no installation is necessary; the portfolio is just a website. As a developer, you may [fork this repo](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) to install it locally in order to build your own version (note that I am not accepting pull requests from forked repos at this time). Then follow the setup instructions below.
1. Requirements:
    * Python 3.13+
    * A Twilio account
    * An AWS account
2. In the root directory, add a .env file with values for the following environment variables:
    * ENV=DEV
    * DJANGO_SECRET_KEY
    * EMAIL_HOST
    * EMAIL_HOST_PASSWORD
    * EMAIL_HOST_USER
    * EMAIL_PORT
    * EMAIL_USE_TLS
    * DEFAULT_FROM_EMAIL
    * TWILIO_ACCOUNT_SID
    * TWILIO_AUTH_TOKEN
    * TWILIO_CALLER_ID
    * AWS_ACCESS_KEY
    * AWS_SECRET_ACCESS_KEY
    * AWS_STORAGE_BUCKET_NAME
3. In the root directory, create a virtual environment (e.g., `python -m venv venv`).
4. Activate the virtual environment (e.g., `source venv/bin/activate`).
5. Install dependencies: `pip install -r requirements.txt`.
6. Run migrations: `python manage.py migrate`.

<br/>

### Usage

You may view my software engineering projects on the Software Engineering page, my AI Prompt Engineering projects on the AI Prompt Engineering page, or my instructional design projects on the Instructional Design page. You may also view the web version of my resume or download the MS Word version on the Resume page. Navigate to the Blog page to check out my thought leadership. Send me a message on the Contact page if you might be interested in working together!

<br/>

## Lessons Learned 

I used the same tech stack to build this portfolio that I use on a daily basis at work, and most of my professional work is more complex than this portfolio. I didn't learn new concepts or tech on this project, but I did challenge myself to explore breaking up the project into multiple applications--core site, portfolio, blog--and to do everything else as simply and DRY as possible.

However, this project does use TailwindCSS version 4, which I have not previously used (my work projects and previous personal projects use version 3). There were some significant changes in version 4. For example, this version no loger uses a `tailwind.config.js` file, so I had to learn the new configuration method using an `@theme` directive. This change was even more glaring because the documentation for the django-tailwind library still referenced `tailwind.config.js`.

In addition, I used the x-intersect plugin for Alpine.js to simplify working with the intersection observer for entrance transitions. In doing so, I learned that having an `x-intersect` property and an `x-transition` property on the same element does not work well; it is best to put `x-intersect` on a container element and apply `x-transition` to the child element.

<br/>

## Author Info

### Ryan Moscoe 

* [Portfolio](https://www.ryanmoscoe.com/)
* [LinkedIn](https://www.linkedin.com/in/ryan-moscoe-8652973/)
* [Github](https://github.com/rmoscoe)

<br/>

## Future Development

In addition to software engineering, AI prompt engineering, and instructional design, I also design tabletop games (board games, card games, and roleplaying games). My roadmap for this portfolio site includes the addition of a Games page to showcase my games.

<br/>

## License

See repo for license information.

<br/>

## Contributing

I am not accepting contributions to this site at this time.