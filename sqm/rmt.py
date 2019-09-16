# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 12:21:03 2018

@author: mshem
"""
from ftplib import FTP

from MySQLdb import connect

from . import env

class sql():
    def __init__(self, address, user, password, database, port=3307, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger= self.debugger)
        self.port = port
        
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        
        self.do_connect()
        
    def do_connect(self):
        self.logger.log("Connecting to server at {}".format(self.address))
        try:
            self.sql = connect(host=self.address, user=self.user,
                               passwd=self.password, db=self.database,
                               port=self.port)
        except Exception as e:
            self.logger.log(e)
            self.sql = None
            
    def update(self, table, fields, values, where):
        cur = self.sql.cursor() 
        if len(fields) == len(values):
            
            equal = []
            
            for i in range(len(fields)):
                equal.append("{}={}".format(fields[i], values[i]))
                
            sql = "UPDATE `{}` SET {} {}".format(table, ", ".join(equal), where)
            self.logger.log(sql)
            

            try:
                cur.execute(sql)
                return True
            except Exception as e:
                self.logger.log(e)
                return False
                
            cur.close()
            self.sql.commit()
            
        else:
            self.logger.log("Number of values and files are not same")
            
    def insert(self, table, fields, values):
        try:
            if self.sql is not None:
                cur = self.sql.cursor()
                fields_str = ", ".join(fields)
                
                values_str = ""
                for value in values:
                    tmp = ""
                    for single_value in value:
                        tmp = "{}, '{}'".format(tmp, single_value)
                    tmp = tmp[2:]
                    
                    values_str = "({}), {}".format(tmp, values_str)
                values_str = values_str[:-2]
                    
                sql = "insert ignore into  `{0}` ({1}) values {2};".format(
                        table, fields_str, values_str)
                
                try:
                    cur.execute(sql)
                except Exception as e:
                    self.logger.log(e)
                    
                cur.close()
                self.sql.commit()
            else:
                self.logger.log("No sql connection")
                return False
        except Exception as e:
            self.logger.log(e)
            return False
            
    def select(self, table, fields="*", where="WHERE 1", groupb=""):
        try:
            cur = self.sql.cursor()
            sql = "SELECT `{0}` from {1} {2} {3}".format(fields, table, where, groupb)
            self.logger.log(sql)
            cur.execute(sql)
            cur.fetchall()
            
            
            ret = []
            for i in cur:
                ln = []
                for u in i:
                    ln.append(u)
                ret.append(ln)
            
            return ret
        except Exception as e:
            self.logger.log(e)
        
    def close(self):
        self.logger.log("Closing connetion to server at {}".format(self.address))
        try:
            if self.sql is not None:
                self.sql.close()
            else:
                self.logger.log("No sql connection")
        except Exception as e:
            self.logger.log(e)


class Ftp():
    def __init__(self, address, user, password, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.address = address
        self.user = user
        self.password = password
        self.do_connect()
        
    def do_connect(self):
        self.logger.log("Connecting to server at {}".format(self.address))
        try:
            self.ftp = FTP(self.address, self.user, self.password)
        except Exception as e:
            self.logger.log(e)
            self.ftp = None
    
    def close(self):
        self.logger.log("Closing connetion to server at {}".format(self.address))
        try:
            if self.ftp is not None:
                self.ftp.quit()
            else:
                self.logger.log("No ftp connection")
        except Exception as e:
            self.logger.log(e)
            
    def cd(self, path):
        self.logger.log("Changinh directory {}".format(path))
        try:
            if self.ftp is not None:
                self.ftp.cwd(path)
            else:
                self.rtc.log("No ftp connection")
        except Exception as e:
            self.logger.log(e)
            
    def mkdir(self, name):
        self.logger.log("Making directory {}".format(name))
        try:
            if self.ftp is not None:
                self.ftp.mkd(name)
            else:
                self.logger.log("No ftp connection")
        except Exception as e:
            self.logger.log(e)
            
            
    def put(self, local_file, remote_file):
        self.logger.log("Putting file({}) to server at {}".format(local_file,
                     self.address))
        try:
            if self.ftp is not None:
                cont = open(local_file,'rb')
                self.ftp.storbinary('STOR {}'.format(remote_file), cont)
                cont.close()
                return True
            else:
                self.logger.log("No ftp connection")
                return False
        except Exception as e:
            self.logger.log(e)
            return False
            
    def ls(self, the_dir):
        self.logger.log("Retrewing list from remote path {}".format(the_dir))
        try:
            if self.ftp is not None:
                ls = []
                self.ftp.retrlines('nlst {}'.format(the_dir), ls.append)
                return(ls)
            else:
                self.logger.log("No ftp connection")
        except Exception as e:
            self.logger.log(e)