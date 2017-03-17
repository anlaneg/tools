#ifndef CALLBACKS_H
#define CALLBACKS_H

#include <stdarg.h>

enum callback_mode
{
    CREAT_MODE,
    REPLICE_MODE,
};

//callback type
typedef int(*callback_fun)(char*resource,char*event,va_list ap);


int notify(char*resource,char*event,...);

/**
 * 注册回调
 */
int subscribe(char*resource,char*event,callback_fun callback,int mode);

int unsubscribe(char*resource,char*event,callback_fun callback);

int unsubscribe_by_resource(char*resource,callback_fun callback);

int unsubscribe_all(callback_fun callback)

#endif
