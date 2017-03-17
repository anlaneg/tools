#ifndef CALLBACKS_H
#define CALLBACKS_H

#include "callback.h"

struct callback_node
{
    char* resource;
    char* event;
    callback_fun call;
    struct callback_node* next;
};



int notify(char*resource,char*event,...)
{
}

int subscribe(char*resource,char*event,callback_fun callback,int mode)
{
    
}

int unsubscribe(char*resource,char*event,callback_fun callback)
{

}

int unsubscribe_by_resource(char*resource,callback_fun callback)
{

}
int unsubscribe_all(callback_fun callback)
{

}

#endif
