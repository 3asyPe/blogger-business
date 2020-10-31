Home -> login/registration "/"
Login "/login"

Blogger
    - Registration "/registration"
    - Home page with offers "/offers"
    - Offer details "/offers/id"
    - Profile "/profile/id" (If can be changed in settings, by default slugified name)

Business
    - Registration "/registration"
    - Explanations for creating offers (animation)
    - Offers "/offers/actions" (created, create new one and see how blogger will see them)
    - Offer details "offers/id"
    - Offer creation "/offers/create"
    - Waiting for applications "/apllications/"
    - Application page "/application/id/"
    - Profile "/profile/id" (If can be changed in settings, by default slugified name)

routes:
    "/"
    ""
    "login"
    "registration"
        for business
            "?type=bu"
        for blogger
            "?type=bl"
    "help/animation"
        for business
            "?type=bu"
        for blogger
            "?type=bl"
    "offers"
        "/id"
        for business:
            "/actions"
            "/create"
        for blogger
    "applications"
        for business:
            "/id"
    "profile/id"
        for business
        for blogger
    "profile/settings"
        for business
        for blogger
    "about"
    "contacts"
    "help"
    "terms-of-use"
    