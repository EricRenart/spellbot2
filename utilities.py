import datetime

class Utilities:
    
    def levels_dict_to_sql_string(levels: dict):
        string = f""
        for lvl in levels.keys():
            val = levels.get(lvl)
            string += f"{lvl} {val},"
        return string
    
    def dict_to_sql_values_pair(kv: dict):
        string = "("
        for key in kv.keys():
            string += f"{key},"
        string += ") VALUES ("
        for value in kv.values():
            string += f"{value},"
        string = string[-1]
        string += ","
        return string
    
    def parenthesized_list(ls: list):
        ls_str = '('
        for elem in ls:
            ls_str += f'{elem},'
        return f'{ls_str})'
    
    def datetime_string():
        return datetime.datetime.now().strftime('%m/%-d/%Y %H:%M:%S.%f')