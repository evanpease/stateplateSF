from flask_table import Table, Col
 
class Results(Table):
    id = Col('Id', show=False)
    name = Col('Restaurant')
    menu_url = Col('Menu URL')
    address = Col('Address')
    sim = Col('Similarity')