#define _POSIX_C_SOURCE 200809L
#include <Ecore.h>
#include <Ecore_Evas.h>
#include <Edje.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
static void tick(Ecore_Evas *ee){ecore_main_loop_iterate_may_block(0);ecore_evas_buffer_pixels_get(ee);struct timespec t={0,16000000};nanosleep(&t,NULL);}
static void wait_for(Ecore_Evas *ee,double seconds){double start=ecore_time_get();while(ecore_time_get()-start<seconds)tick(ee);}
static double cpu(void){struct rusage r;getrusage(RUSAGE_SELF,&r);return r.ru_utime.tv_sec+r.ru_utime.tv_usec/1e6+r.ru_stime.tv_sec+r.ru_stime.tv_usec/1e6;}
static void save(Ecore_Evas *ee,Evas *e,const char *dir,const char *name){char file[1024];snprintf(file,sizeof(file),"%s/%s.png",dir,name);Evas_Object *im=evas_object_image_add(e);evas_object_image_size_set(im,960,540);evas_object_image_alpha_set(im,0);evas_object_image_data_copy_set(im,(void*)ecore_evas_buffer_pixels_get(ee));if(!evas_object_image_save(im,file,NULL,"compress=1"))exit(3);evas_object_del(im);}
int main(int argc,char **argv){
 if(argc!=3)return 2;ecore_evas_init();edje_init();Ecore_Evas *ee=ecore_evas_buffer_new(960,540);if(!ee)return 3;Evas *e=ecore_evas_get(ee);Evas_Object *wall=edje_object_add(e);
 if(!edje_object_file_set(wall,argv[1],"e/desktop/background")){fprintf(stderr,"wallpaper: %s\n",edje_load_error_str(edje_object_load_error_get(wall)));return 4;}
 evas_object_resize(wall,960,540);evas_object_show(wall);wait_for(ee,.05);
 for(int n=0;n<16;n++){char name[64];snprintf(name,sizeof(name),"frame-%03d",n);save(ee,e,argv[2],name);wait_for(ee,.25);}
 double start=ecore_time_get(),usage=cpu();wait_for(ee,4);printf("BENCH animated percent_one_core=%.2f size=960x540\n",(cpu()-usage)/(ecore_time_get()-start)*100);
 edje_object_signal_emit(wall,"ami,pause","host");edje_object_message_signal_process(wall);save(ee,e,argv[2],"paused-before");start=ecore_time_get();usage=cpu();wait_for(ee,1);double paused_elapsed=ecore_time_get()-start,paused_cpu=cpu()-usage;save(ee,e,argv[2],"paused-after");printf("BENCH paused percent_one_core=%.2f size=960x540\n",paused_cpu/paused_elapsed*100);
 edje_object_signal_emit(wall,"ami,resume","host");edje_object_message_signal_process(wall);wait_for(ee,1.3);save(ee,e,argv[2],"resumed");
 puts("PASS native wallpaper frame/pause/resume capture completed");ecore_evas_free(ee);edje_shutdown();ecore_evas_shutdown();return 0;
}
