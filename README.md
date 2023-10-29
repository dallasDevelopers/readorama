# Readorama: your literacy universe
## Group name: Dallas Developers Club
## Group members:
- Adam Muhammad
- Rafi Ardiel Erinaldi
- Bramantyo Priyo Utomo
- Cyrill Adrian Wicaksono
- Omar Khalif Muchzi

## Story of the application:
**Background:**
Readorama is a dedicated online platform designed with a mission to elevate literacy rates among Indonesians. With a deep commitment to empowering individuals through the power of reading and education, Readorama aims to be a transformative force in Indonesia's journey towards improved literacy.

**Our Mission:**
At Readorama, our primary goal is to provide accessible, engaging, and high-quality reading materials and resources to people of all ages and backgrounds across Indonesia. We believe that literacy is the cornerstone of personal and societal development, and we are determined to make a positive impact on our nation's literacy landscape.

**User-Friendly Interface:**
Our website is designed to be user-friendly and accessible, ensuring that individuals with varying levels of digital literacy can easily navigate and benefit from our resources.


## Roles
1. User 
2. Admin

## List of Modules 
1. Login and Sign-up Page (authentication)


1. Landing Page/ Main Page (user & admin)
Navbar: 
2. Book: (Dropdown)
- book search
- top rated books
- review books 

3. Account: (Dropdown )
- Home 
- Profile 
- Read List
- Likes

4. Review page


## Source of the book catalog dataset:
[Kaggle](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019)


### Flow to run program:
1. migrate all migrations

2. create superuser to login as admin, by running this command:

```
py manage.py createsuperuser
```

3. load data fixture by running this command:

```
py manage.py loaddata bookdatasjson.json
```

### Web Flow:
1. add book to wishlist/mark the book as read
2. open wishlist(if the book added to wishlist) you can remove from wishlist or mark it as read
3. open read books menu to give review
4. "Your Review" menu is to show all the books that have been reviewed