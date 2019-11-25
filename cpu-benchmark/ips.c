
#include <stdlib.h>
#include <pthread.h>

#define CACHE_LINE_SIZE 64

typedef void (*task_func_t)(void*);

struct task{
	task_func_t func;
	void* args;
	pthred_t id;
}__attribute__((__aligned__(CACHE_LINE_SIZE)));

struct thread_group{
	int count;
	unsigned int offset;
	char pading[CACHE_LINE_SIZE - sizeof(int) - sizeof(unsigned int)];
	struct task task[0];
};

void cpu_bound()
{
	register unsigned long i=0;
	for (i=0;i<(1UL<<33);i++) {
		__asm__ ("nop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\n");
	}
}

struct thread_group* create_thread_group(void (*func)(),int size)
{
	int i ;
	struct thread_group* group;

	if(size <= 0)
	{
		return NULL;
	}

	group = malloc(sizeof(*group) + CACHE_LINE_SIZE+ sizeof(struct task)*size);
	if(!group)
	{
		return NULL;
	}

	group->count = size;
	group->offset =  (CACHE_LINE_SIZE - (group % CACHE_LINE_SIZE));
	group = (char*)group + group ->offset;

	assert(group % CACHE_LINE_SIZE == 0);
	assert(&group->task[0] % CACHE_LINE_SIZE == 0);

	for(i = 0 ; i < size; ++i)
	{
		struct task * self= &(group->task[i]);
		self->func = func;
		self->args = (void*)i;
	}

	return group;
}

static void* thread_run_wrap(void* args)
{
}

void stop_thread_group(struct thread_group*group,int count)
{
	int i ;
	assert(group);
	assert(count >= 0 && group->count >= count);
	for(i = 0 ; i < count; ++i)
	{
		//join thread
	}	
}

int start_thread_group(struct thread_group*group)
{
	int i;
	assert(group);
	for(i = 0 ; i < group->count;++i)
	{
		if(pthread_create(&group->task[i].id, NULL,thread_run_wrap,&group->task[i]))
		{
			goto STOP_THREAD;
		}
	}

	return  0;
STOP_THREAD:
	stop_thread_group(group,i);
}

int run_thread_group(struct thread_group*group)
{

}

int main() {
	cpu_bound();
	return 0;
}

