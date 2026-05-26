"""
Seed script to populate BlogPlatform with sample data.
Run: python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogplatform.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Comment, Like

print("🌱 Seeding BlogPlatform with sample data...\n")

# ── Create Admin User ──────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    admin = User.objects.get(username='admin')
    print("ℹ️  Admin user already exists.")

# ── Create Sample Users ────────────────────────────────────────
user_data = [
    ('alice', 'alice@example.com', 'Alice123!'),
    ('bob', 'bob@example.com', 'Bob12345!'),
    ('carol', 'carol@example.com', 'Carol123!'),
]
users = {}
for username, email, password in user_data:
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password)
        print(f"✅ User created: {username}")
    else:
        u = User.objects.get(username=username)
    users[username] = u

# ── Create Categories ──────────────────────────────────────────
categories_data = [
    ('Technology', 'tech-tips', 'Insights on the latest in technology, programming, and digital trends.', '#6C63FF'),
    ('Science', 'science', 'Exploring the wonders of science and discovery.', '#43C6AC'),
    ('Lifestyle', 'lifestyle', 'Tips and ideas for living a fulfilling, balanced life.', '#FF6584'),
    ('Design', 'design', 'UI/UX design, creativity, and visual aesthetics.', '#FFD700'),
    ('Career', 'career', 'Personal growth, career tips, and professional development.', '#FF8C42'),
]
cats = {}
for name, slug, desc, color in categories_data:
    cat, created = Category.objects.get_or_create(
        slug=slug, defaults={'name': name, 'description': desc, 'color': color}
    )
    cats[slug] = cat
    if created:
        print(f"✅ Category: {name}")

# ── Create Sample Posts ────────────────────────────────────────
posts_data = [
    {
        'title': 'Getting Started with Python Django in 2025',
        'author': users['alice'],
        'category': cats['tech-tips'],
        'featured_image_url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800',
        'body': """Django remains one of the most powerful and beginner-friendly web frameworks available today. Whether you're building a simple blog or a complex SaaS platform, Django's "batteries included" philosophy makes development fast and enjoyable.

In this guide, we'll walk through setting up your first Django project from scratch. We'll cover virtual environments, project structure, app creation, and how Django's MVC (Model-View-Controller) pattern works in practice.

First, let's install Django using pip. It's recommended to create a virtual environment first to isolate your project's dependencies from other Python projects on your machine.

Once installed, creating a new project is as simple as running the `django-admin startproject` command. Django will scaffold the entire project structure for you, complete with settings, URL routing, and the WSGI application entry point.

From there, you can start building your first app, define your data models, and run migrations to create your database tables. Django's ORM (Object Relational Mapper) is incredibly powerful — it lets you write Python code instead of raw SQL, yet still have full control over your database.
""",
    },
    {
        'title': 'The Art of Clean UI Design: Less Is More',
        'author': users['bob'],
        'category': cats['design'],
        'featured_image_url': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800',
        'body': """Great design isn't about adding more — it's about removing everything that doesn't belong. The best interfaces feel invisible, guiding users effortlessly to their goals without friction or confusion.

The principle of visual hierarchy is fundamental. By controlling the size, color, and weight of elements, designers direct the user's attention to what matters most. Every element on the screen should have a purpose, and if you can't articulate why something is there, it probably shouldn't be.

Whitespace — often called negative space — is one of the most underutilised tools in a designer's arsenal. Giving elements room to breathe improves readability, reduces cognitive load, and makes interfaces feel premium and trustworthy.

Color palettes should be intentional and restrained. A palette of 2-3 main colors with clear purposes (primary, accent, neutral) will always outperform a rainbow of competing hues. Dark mode has become increasingly popular, not just for aesthetics, but because it genuinely reduces eye strain in low-light environments.

Typography is the backbone of any great design. Choosing the right typeface, scale, and spacing can transform an average interface into something that feels polished and professional.
""",
    },
    {
        'title': 'How to Build Sustainable Morning Routines That Actually Stick',
        'author': users['carol'],
        'category': cats['lifestyle'],
        'featured_image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800',
        'body': """Morning routines are everywhere online — from the 5 AM club to elaborate journaling rituals. But the truth is, a sustainable morning routine looks different for everyone. The key isn't to copy someone else's routine; it's to design one that aligns with your own life, values, and goals.

Start small. Adding one intentional habit to your morning is far more powerful than trying to overhaul everything at once. Research in behavioral science consistently shows that habit stacking — attaching a new habit to an existing one — dramatically increases success rates.

Hydration is perhaps the single most impactful thing you can do right after waking. A glass of water rehydrates your cells after 7-8 hours without fluids and kickstarts your metabolism. It's simple, free, and backed by science.

Movement doesn't have to mean a full gym session. Even 10 minutes of stretching, yoga, or a short walk can elevate your mood, boost cognitive function, and prepare you for the day ahead. The goal is to signal to your body and mind that today is starting intentionally.

Protecting the first 30-60 minutes from screens — especially social media and email — is transformative. Use that time for yourself before allowing the external world to set your agenda.
""",
    },
    {
        'title': 'Black Holes: Understanding the Universe\'s Most Mysterious Objects',
        'author': admin,
        'category': cats['science'],
        'featured_image_url': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800',
        'body': """Black holes have captivated scientists and science enthusiasts alike for over a century. First predicted by Einstein's General Theory of Relativity in 1915, these cosmic phenomena represent some of the most extreme physics in the universe.

A black hole forms when a massive star runs out of fuel and collapses under its own gravity. The resulting object is so dense that nothing — not even light — can escape its gravitational pull beyond a boundary called the event horizon. Once something crosses this threshold, it's gone from our observable universe forever.

The singularity at the center of a black hole is where our understanding of physics breaks down. Here, matter is compressed to an infinitely small point with infinite density, and the equations of general relativity produce results that no longer make physical sense. This breakdown suggests we need a theory of quantum gravity — a unification of quantum mechanics and general relativity — to fully understand what happens inside.

In 2019, humanity captured the first-ever image of a black hole's event horizon, belonging to the supermassive black hole in the galaxy M87. This historic image, produced by the Event Horizon Telescope collaboration, showed the distinctive glowing ring of superheated gas surrounding the shadow of the black hole — exactly as Einstein's equations predicted.

Closer to home, at the center of our own Milky Way galaxy, lies Sagittarius A*, a supermassive black hole with the mass of approximately 4 million suns. In 2022, scientists captured its image for the first time, confirming theories about our galaxy's turbulent heart.
""",
    },
    {
        'title': 'Negotiating Your Salary: A Data-Driven Approach',
        'author': users['alice'],
        'category': cats['career'],
        'featured_image_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800',
        'body': """Most people leave significant money on the table throughout their careers simply because they don't negotiate. Studies consistently show that less than 40% of professionals negotiate their salary offers, yet those who do earn substantially more over the course of their career.

The first step is research. Before any negotiation conversation, thoroughly research market rates for your role, experience level, industry, and location. Platforms like Glassdoor, Levels.fyi, LinkedIn Salary, and industry-specific surveys provide valuable data points. Walk into the conversation knowing your market value.

Frame the negotiation around value, not need. Employers don't give raises because employees are underpaid — they do so because they want to retain people who deliver results. Lead with the value you bring: specific achievements, quantifiable impact, and skills that are difficult to replace.

Always let the employer make the first offer if possible. Research shows that the first number anchors the negotiation, and when companies reveal their range first, you gain valuable information about how much room exists to negotiate upward.

The power of silence is vastly underrated. After you make your ask, resist the urge to fill the silence. Experienced negotiators know that the first person to speak after a salary request often concedes ground unnecessarily.

Remember: salary is just one dimension of compensation. Benefits, vacation time, remote work flexibility, professional development budgets, and equity can all be negotiated. Think of your total compensation package, not just the base number.
""",
    },
    {
        'title': 'CSS Grid vs Flexbox: When to Use Which',
        'author': users['bob'],
        'category': cats['tech-tips'],
        'featured_image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',
        'body': """Both CSS Grid and Flexbox are powerful layout tools, and one of the most common questions developers ask is: which one should I use? The short answer is that they solve different problems, and knowing when to reach for each is a skill that separates good developers from great ones.

Flexbox is a one-dimensional layout system. It operates along a single axis — either a row or a column — making it perfect for distributing space among items within a single container. Navigation bars, button groups, card content alignment, and centering elements are all classic Flexbox use cases.

CSS Grid, on the other hand, is two-dimensional. It controls both rows and columns simultaneously, making it ideal for overall page layouts, image galleries, dashboards, and any case where you need to align elements across both axes at once.

A useful mental model: use Flexbox for components and small-scale layouts, use Grid for larger, page-level layouts. But this isn't a hard rule. Many excellent layouts combine both — a Grid for the overall page structure, and Flexbox inside individual grid items for their internal layout.

Grid's `auto-fit` and `auto-fill` with `minmax()` is arguably one of the most powerful responsive design tools available, letting you create fluid, responsive grids with a single line of CSS and no media queries.

Both tools are now supported in all modern browsers, so there's no reason to avoid either. Experiment with them, understand their strengths, and you'll find yourself reaching for the right tool instinctively.
""",
    },
]

created_posts = []
for p_data in posts_data:
    slug_base = p_data['title'].lower().replace(' ', '-').replace("'", '').replace(':', '').replace(',', '')[:60]
    if not Post.objects.filter(slug=slug_base).exists():
        post = Post.objects.create(**p_data)
        created_posts.append(post)
        print(f"✅ Post: {p_data['title'][:50]}...")
    else:
        created_posts.append(Post.objects.get(slug=slug_base))
        print(f"ℹ️  Post exists: {p_data['title'][:50]}...")

# ── Add Comments ───────────────────────────────────────────────
comments_data = [
    (created_posts[0], users['bob'], "Really helpful intro! I've been wanting to learn Django for a while and this is a great starting point."),
    (created_posts[0], users['carol'], "Great write-up! Do you have a follow-up post planned on Django REST Framework?"),
    (created_posts[0], admin, "Thanks for the positive feedback! A REST Framework tutorial is definitely on the way."),
    (created_posts[1], users['alice'], "This resonates so much. I've been guilty of cluttering my designs — the whitespace advice is gold."),
    (created_posts[1], users['carol'], "The point about dark mode reducing eye strain is spot on. I switched my entire workflow to dark mode last year."),
    (created_posts[2], users['bob'], "I tried waking up at 5 AM and it was a disaster. You're right — starting small is the key!"),
    (created_posts[3], users['alice'], "The image from the Event Horizon telescope was one of the most exciting moments in science I've witnessed."),
    (created_posts[3], users['carol'], "Absolutely fascinating. The fact that Hawking radiation is still theoretical blows my mind."),
    (created_posts[4], users['bob'], "Negotiated my first salary after reading tips like these. Got 15% more than the initial offer!"),
    (created_posts[5], users['carol'], "Perfect breakdown. I always default to Flexbox but Grid's auto-fill feature is a game changer."),
]

for post, author, body in comments_data:
    if not Comment.objects.filter(post=post, author=author, body=body).exists():
        Comment.objects.create(post=post, author=author, body=body)

print(f"✅ Comments added")

# ── Add Likes ──────────────────────────────────────────────────
like_data = [
    (created_posts[0], [users['bob'], users['carol'], admin]),
    (created_posts[1], [users['alice'], users['carol']]),
    (created_posts[2], [users['alice'], users['bob'], admin]),
    (created_posts[3], [users['alice'], users['bob'], users['carol']]),
    (created_posts[4], [users['bob'], users['carol']]),
    (created_posts[5], [users['alice'], admin]),
]
for post, likers in like_data:
    for user in likers:
        Like.objects.get_or_create(post=post, user=user)

print("✅ Likes added")

print("\n" + "="*55)
print("🎉 BlogPlatform seeded successfully!")
print("="*55)
print("🌐 Run: python manage.py runserver")
print("🔗 Open: http://127.0.0.1:8000")
print()
print("👤 Admin:  admin     / admin123")
print("👤 User 1: alice     / Alice123!")
print("👤 User 2: bob       / Bob12345!")
print("👤 User 3: carol     / Carol123!")
print("="*55)
