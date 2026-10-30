#define _POSIX_C_SOURCE 200809L
#include <Ecore.h>
#include <Ecore_Evas.h>
#include <Edje.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
static Evas_Object *load(Evas *e,const char *f,const char *g,int x,int y,int w,int h){
 Evas_Object *o=edje_object_add(e);if(!edje_object_file_set(o,f,g)){fprintf(stderr,"LOAD %s: %s\n",g,edje_load_error_str(edje_object_load_error_get(o)));exit(1);}evas_object_move(o,x,y);evas_object_resize(o,w,h);evas_object_show(o);return o;
}
static void tick(Ecore_Evas *ee){ecore_main_loop_iterate_may_block(0);ecore_evas_buffer_pixels_get(ee);struct timespec ts={0,16000000};nanosleep(&ts,NULL);}
static double cpu(void){struct rusage r;getrusage(RUSAGE_SELF,&r);return r.ru_utime.tv_sec+r.ru_utime.tv_usec/1e6+r.ru_stime.tv_sec+r.ru_stime.tv_usec/1e6;}
static void save(Ecore_Evas *ee,Evas *e,const char *path,int w,int h){const void *px=ecore_evas_buffer_pixels_get(ee);Evas_Object *im=evas_object_image_add(e);evas_object_image_size_set(im,w,h);evas_object_image_alpha_set(im,0);evas_object_image_data_copy_set(im,(void*)px);if(!evas_object_image_save(im,path,NULL,"compress=2"))exit(3);evas_object_del(im);}
int main(int argc,char **argv){
 if(argc!=5){fprintf(stderr,"theme wallpaper output-directory capture|bench\n");return 2;}
 int bench=argv[4][0]=='b';int w=bench?1920:960,h=bench?1080:540;
 ecore_evas_init();edje_init();ecore_animator_frametime_set(1.0/30.0);edje_frametime_set(1.0/30.0);
 Ecore_Evas *ee=ecore_evas_buffer_new(w,h);if(!ee)return 1;Evas *e=ecore_evas_get(ee);
 Evas_Object *wall=load(e,argv[2],"e/desktop/background",0,0,w,h);
 Evas_Object *border=load(e,argv[1],"e/widgets/border/default/border",w/12,h/6,w*3/4,h*2/5);
 edje_object_part_text_set(border,"e.text.title","Ami — material motion study");
 Evas_Object *client=load(e,argv[1],"ami/preview-panel",0,0,20,20);edje_object_part_swallow(border,"e.swallow.client",client);
 edje_object_signal_emit(border,"e,state,focused","e");edje_object_message_signal_process(border);
 for(int i=0;i<3;i++){Evas_Object *b=load(e,argv[1],"elm/button/base/default",w/8+i*w/5,h/3,w/6,h/16);edje_object_part_text_set(b,"elm.text",i==0?"Materials":i==1?"Motion":"Still option");edje_object_signal_emit(b,"elm,state,text,visible","elm");edje_object_message_signal_process(b);}
 Evas_Object *shelf=load(e,argv[1],"e/shelf/default/base",w/8,h*5/6,w*3/4,h/9);
 edje_object_signal_emit(shelf,"e,state,orientation,bottom","e");edje_object_message_signal_process(shelf);
 const char *icons[]={"user-home","system-file-manager","utilities-terminal","preferences-system","multimedia-player","user-trash"};
 for(int i=0;i<6;i++) {char path[512];snprintf(path,sizeof(path),"/work/icons/%s.png",icons[i]);Evas_Object *im=evas_object_image_filled_add(e);evas_object_image_file_set(im,path,NULL);evas_object_move(im,w/5+i*w/10,h*5/6-h/90);evas_object_resize(im,h/9,h/9);evas_object_show(im);}
 if(bench){
  double warm=ecore_time_get();while(ecore_time_get()-warm<10.05)tick(ee);


  for(int phase=0;phase<2;phase++){
   if(phase){edje_object_signal_emit(wall,"ami,pause","host");edje_object_signal_emit(border,"ami,pause","host");edje_object_message_signal_process(wall);edje_object_message_signal_process(border);}
   double begin=ecore_time_get(),usage=cpu();int ticks=0;
   while(ecore_time_get()-begin<4){tick(ee);ticks++;}
   double elapsed=ecore_time_get()-begin;
   printf("BENCH %s wall=%.3f cpu=%.3f percent_one_core=%.2f ticks=%d size=%dx%d\n",phase?"paused":"animated",elapsed,cpu()-usage,(cpu()-usage)/elapsed*100,ticks,w,h);
  }
 }else{
  double begin=ecore_time_get();
  for(int i=0;i<85;i++){while(ecore_time_get()-begin<i/6.0)tick(ee);char path[1024];snprintf(path,sizeof(path),"%s/frame-%03d.png",argv[3],i);save(ee,e,path,w,h);}
  edje_object_signal_emit(wall,"ami,pause","host");edje_object_signal_emit(border,"ami,pause","host");edje_object_message_signal_process(wall);edje_object_message_signal_process(border);
  char path[1024];snprintf(path,sizeof(path),"%s/paused-before.png",argv[3]);save(ee,e,path,w,h);
  double begin_pause=ecore_time_get();while(ecore_time_get()-begin_pause<1)tick(ee);
  snprintf(path,sizeof(path),"%s/paused-after.png",argv[3]);save(ee,e,path,w,h);
  edje_object_signal_emit(wall,"ami,resume","host");edje_object_signal_emit(border,"ami,resume","host");edje_object_message_signal_process(wall);edje_object_message_signal_process(border);
  double begin_resume=ecore_time_get();while(ecore_time_get()-begin_resume<11.2)tick(ee);
  snprintf(path,sizeof(path),"%s/resumed.png",argv[3]);save(ee,e,path,w,h);
  printf("CAPTURE_COMPLETE 85 native frames; cycle 14s; pause/resume sampled\n");
 }
 ecore_evas_free(ee);edje_shutdown();ecore_evas_shutdown();return 0;
}
