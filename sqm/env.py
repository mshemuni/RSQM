# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 09:08:25 2019

@author: msh
"""


from os.path import expanduser
from os.path import exists
from os.path import isfile
from os.path import dirname
from os.path import basename
from os.path import realpath
from os.path import splitext
from os.path import abspath
from os.path import getsize

from os import walk
from os import remove
from os import mkdir

from glob import glob

from gzip import open as gopen

from shutil import copyfileobj
from shutil import copy2
from shutil import move

from datetime import datetime

from getpass import getuser

from platform import uname
from platform import system

from inspect import currentframe
from inspect import getouterframes

from  numpy import genfromtxt
from  numpy import savetxt
from  numpy import asarray

class Logger():
    def __init__(self, verb=False, debugger=False):
        self.verb = verb
        self.log_dir = abspath("{}/mylog/".format(expanduser("~")))
        self.log_file = abspath("{}/log.my".format(self.log_dir))
        self.mini_log_file = abspath("{}/mlog.my".format(self.log_dir))
        self.debugger = debugger
        
        if not((not isfile(self.log_dir)) and exists(self.log_dir)):
            mkdir(self.log_dir)
        
    def time_stamp(self):
        return(str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")))
        
    def time_stamp_(self):
        return(str(datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")))
    
    def user_name(self):
        return(str(getuser()))
    
    def system_info(self):
        si = uname()
        return("{}, {}, {}, {}".format(si[0], si[2], si[5], self.user_name()))

    def caller_function(self, pri=False):
        curframe = currentframe()
        calframe = getouterframes(curframe, 2)
        caller = calframe
        self.system_info()
        if pri:
            return("{}>{}>{}".format(caller[0][3], caller[1][3], caller[2][3]))
        else:
            return(caller)
            
    def print_if(self, text):
        if self.verb:
            print("[{}|{}]{}".format(self.time_stamp(), self.system_info(),
                   text))
            
    def log(self, text):
        if self.debugger:
            log_file = open(self.log_file, "a")
            log_file.write("Time: {}\n".format(self.time_stamp()))
            log_file.write("System Info: {}\n".format(self.system_info()))
            log_file.write("Log: {}\n".format(text))
            log_file.write("Function: {}\n\n\n".format((self.caller_function())))
            log_file.close()
            
            self.mini_log(text)
        self.print_if(text)
        
    def mini_log(self, text):
        mini_log_file = open(self.mini_log_file, "a")
        mini_log_file.write("[{}|{}] --> {}\n".format(self.time_stamp(),
                            self.system_info(), text))
        mini_log_file.close()
        
    def dump_mlog(self):
        mini_log_file = open(self.mini_log_file, "w")
        mini_log_file.close()
        
    def dump_log(self):
        log_file = open(self.log_file, "w")
        log_file.close()
        
    def is_it_windows(self):
        return(system() == 'Windows')
        
    def is_it_linux(self):
        return(system() == 'Linux')
        
    def is_it_other(self):
        return(not (self.is_it_linux() or self.is_it_windows()))
        
    def beep(self):
        print("\a")
        
    def not_none(self, value):
        return not value is None
        
        
class File():
    
    def __init__(self, verb=False):
        self.verb = verb
        self.logger = Logger(verb=verb)
            
    def get_size(self, src):
        src = self.abs_path(src)
        self.logger.log("Getting file size for {}".format(src))
        try:
            if self.is_file(src):
                return(getsize(src))
        except Exception as e:
            self.logger.log(e)
        
    def abs_path(self, path):
        self.logger.log("Correcting path for {}".format(path))
        try:
            return(abspath(path))
        except Exception as e:
            self.logger.log(e)
            

    def list_of_files(self, src, ext="*"):
        src = self.abs_path(src)
        self.logger.log("Getting list of files")
        try:
            if self.is_dir(src):
                pt = self.abs_path("{}/{}".format(src, ext))
                return(sorted(glob(pt)))
        except Exception as e:
            self.logger.log(e)
            
    def list_of_dirs(self, src, exc="bdf"):
        src = self.abs_path(src)
        self.logger.log("Getting list of files")
        try:
            if self.is_dir(src):
                dirs = sorted([self.abs_path(x[0]) for x in walk(src)])
                dirs = dirs[1:]
                dirs = [ x for x in dirs if exc not in x ]
                return(dirs)
        except Exception as e:
            self.logger.log(e)  
            
    def is_file(self, src):
        src = self.abs_path(src)
        self.logger.log("Checking if file {0} exist".format(src))
        try:
            return(isfile(src))
        except Exception as e:
            self.logger.log(e)
            return(False)
        
    def is_dir(self, src):
        src = self.abs_path(src)
        self.logger.log("Checking if directory {0} exist".format(src))
        try:
            return((not self.is_file(src)) and exists(src))
        except Exception as e:
            self.logger.log(e)
            return(False)
    
    def get_home_dir(self):
        self.logger.log("Getting Home dir path")
        try:
            return(self.abs_path(expanduser("~")))
        except Exception as e:
            self.logger.log(e)
    
    def get_base_name(self, src):
        src = self.abs_path(src)
        self.logger.log("Finding path and file name for {0}".format(src))
        try:
            pn = dirname(realpath(src))
            fn = basename(realpath(src))
            return(pn, fn)
        except Exception as e:
            self.logger.log(e)
    
    def get_extension(self, src):
        self.logger.log("Finding extension for {0}".format(src))
        try:
            return(splitext(src))
        except Exception as e:
            self.logger.log(e)
            
    def split_file_name(self, src):
        src = self.abs_path(src)
        self.logger.log("Chopping path {0}".format(src))
        try:
            path, name = self.get_base_name(src)
            name , extension = self.get_extension(name)
            return(path, name, extension)
        except Exception as e:
            self.logger.log(e)
            
    def cp(self, src, dst):
        src = self.abs_path(src)
        dst = self.abs_path(dst)
        self.logger.log("Copying file {0} to {1}".format(src, dst))
        try:
            copy2(src, dst)
        except Exception as e:
            self.logger.log(e)
            
    def rm(self, src):
        src = self.abs_path(src)
        self.logger.log("Removing file {0}".format(src))
        try:
            remove(src)
        except Exception as e:
            self.logger.log(e)
            
    def mv(self, src, dst):
        src = self.abs_path(src)
        dst = self.abs_path(dst)
        self.logger.log("Moving file {0} to {1}".format(src, dst))
        try:
            move(src, dst)
        except Exception as e:
            self.logger.log(e)
            
    def mkdir(self, path):
        path = self.abs_path(path)
        try:
            if not self.is_dir:
                mkdir(path)
        except Exception as e:
            self.logger.log(e)
            
    def read_array(self, src, dm=" ", dtype=float):
        src = self.abs_path(src)
        self.logger.log("Reading {0}".format(src))
        try:
            if dtype == None:
                return(genfromtxt(src, comments='#', delimiter=dm))
            else:
                return(genfromtxt(src, comments='#', delimiter=dm,
                                  dtype=dtype))
        except Exception as e:
            self.logger.log(e)
            
    def write_array(self, src, arr, dm=" ", h=""):
        src = self.abs_path(src)
        self.logger.log("Writing to {0}".format(src))
        try:
            arr = asarray(arr)
            savetxt(src, arr, delimiter=dm, newline='\n', header=h)
        except Exception as e:
            self.logger.log(e)
            
    def czip(self, in_file, out_file):
        self.logger.log("Creating compressed file {0}".format(in_file))
        try:
            with open(in_file, 'rb') as f_in, gopen(out_file, 'wb') as f_out:
                copyfileobj(f_in, f_out)
            return True
        except Exception as e:
            self.logger.log(e)
            return False