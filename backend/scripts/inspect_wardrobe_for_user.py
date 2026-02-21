from app.config.db import users_collection, wardrobe_collection

def main(email='satya69+autotest@gmail.com'):
    u = users_collection.find_one({'email': email})
    if not u:
        print('User not found:', email)
        return
    uid = str(u.get('_id'))
    print('user id:', uid)
    items = list(wardrobe_collection.find({'user_id': uid}))
    print('wardrobe items:', len(items))
    for it in items:
        print('-', it.get('image_path'))

if __name__ == '__main__':
    main()
