#!/usr/bin/env python3
"""
This module contains the entry point of the command interpreter for the AirBnB Clone project.
"""

import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB Clone project."""
    
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel, 
        "User": User, 
        "State": State, 
        "City": City, 
        "Amenity": Amenity, 
        "Place": Place, 
        "Review": Review
    }
    
    def emptyline(self):
        """Called when an empty line is entered."""
        pass
    
    def default(self, line):
        """Called on an input line when the command prefix is not recognized."""
        try:
            cls_name, action = line.split(".", 1)
            cls_name = cls_name.strip()
            action = action.strip()
            if cls_name in self.classes:
                if "(" in action and ")" in action:
                    method_name, args = action.split("(", 1)
                    args = args[:-1].strip()
                    if method_name == "all":
                        self.do_all(f"{cls_name} {args}")
                    elif method_name == "count":
                        self.do_count(f"{cls_name} {args}")
                    elif method_name == "show":
                        self.do_show(f"{cls_name} {args}")
                    elif method_name == "destroy":
                        self.do_destroy(f"{cls_name} {args}")
                    elif method_name == "update" and ',' in args:
                        id_str, update_args = args.split(',', 1)
                        self.do_update(f"{cls_name} {id_str.strip()} {update_args.strip()}")
                    elif method_name == "update" and isinstance(eval(args), dict):
                        id_str, update_args = args.split(',', 1)
                        self.do_update(f"{cls_name} {id_str.strip()} {update_args.strip()}")
                    else:
                        print("** Unknown syntax: {}".format(action))
                else:
                    print("** Unknown syntax: {}".format(action))
            else:
                print("** class doesn't exist **")
        except:
            print("** Unknown syntax: {}".format(line))

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it to JSON file and print the id."""
        if not arg:
            print("** class name missing **")
        elif arg in self.classes:
            new_instance = self.classes[arg]()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Show string representation of an instance based on the class name and id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            try:
                print(storage.all()[key])
            except:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            try:
                del storage.all()[key]
                storage.save()
            except:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""
        args = shlex.split(arg)
        if len(args) == 0:
            print([str(value) for key, value in storage.all().items()])
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            print([str(value) for key, value in storage.all().items() if key.split('.')[0] == args[0]])

    def do_count(self, arg):
        """Count the number of instances of a class."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            count = len([value for key, value in storage.all().items() if key.split('.')[0] == args[0]])
            print(count)

    def do_update(self, arg):
        """Update an instance based on the class name and id by adding or updating attribute."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = args[0] + "." + args[1]
            try:
                instance = storage.all()[key]
                attr = args[2]
                val = args[3]
                setattr(instance, attr, val)
                instance.save()
            except:
                print("** no instance found **")

    def emptyline(self):
        """Called when an empty line is entered."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()