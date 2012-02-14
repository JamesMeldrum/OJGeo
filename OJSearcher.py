'''
Created on Nov 29, 2011

@author: John
'''

class Searcher(object):
    '''
    classdocs
    '''
    def search_input(self,search_string,geoCoords):
        
        cleaned_search_string = self.clean_search_string(search_string)
        db_region_id = self.map_coords(geoCoords)
        self.save_search_string(cleaned_search_string,db_region_id)
        db_search_query = self.map_search_string(search_string)
        result_list = self.get_db_results(db_region_id,db_search_query)
        return result_list
    
    def clean_search_string(self,search_string):
        
        return search_string    
    
    def get_db_results(self,db_region_id,db_search_query):
        # Needs to return a list of results
        result_list = []
        return result_list
    
    def map_search_string(self,search_string):
        db_search_query = "select * from database where blah is blah"
        return db_search_query
    
    def map_coords(self,geoCoords):
        return geoCoords
    
    def __init__(self):
        self.result_limit = 10
        self.search_string_db_name = "search_string_database.db"
        
    def save_search_string(self,cleaned_search_string,db_region_id):
        from sqlite3 import dbapi2 as sqlite
        from datetime import datetime
        now = datetime.now()
        search_string_con = sqlite.connect(self.search_string_db_name)
        s_c = search_string_con.cursor()
        s_c.execute("insert into search_string_table(search_string,db_region_id,DT_entered) values ('%s','%s','%s')" % (cleaned_search_string,db_region_id,now))
        return
    
    def create_tables(self):
        from sqlite3 import dbapi2 as sqlite
        con = sqlite.connect(self.search_string_db_name)
        c = con.cursor()
        c.execute("create table if not exists search_string_table(search_string,db_region_id,DT_entered)")
        c.execute("create table if not exists search_mapping_table(category_name,service_type,category_name_id,service_type_id)")
        con.commit()
        
    def insert_mapping_data(self,category_list,service_type_list,cat_name_id):
        from sqlite3 import dbapi2 as sqlite
        con = sqlite.connect(self.search_string_db_name)
        c = con.cursor()
        service_type_id =0 #
        cat_name_id =0 
        for service in service_type_list
        for category in category_list:
            c.execute("insert into search_mapping_table(category_name,")
            i+=1
        return