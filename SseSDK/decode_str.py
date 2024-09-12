# # encoding=utf-8
#
# from util.base93 import decode
#
#
# def decode_quote(msg):
#     res_list = msg.split("\x03")
#     if res_list[-1] == '':
#         res_list.remove('')
#     for m in range(len(res_list)):
#         split_list = res_list[m].split("\x02")
#         if split_list[-1] == '':
#             split_list.remove('')
#         for i in range(len(split_list)):
#             str_split = split_list[i].split("=")
#             for j in str_split:
#                 split_decode = decode(str_split[1])
#                 print(split_decode)
#
#
# str_code = "p=#%Aop=#%Kq=Z2t=2<YHf=Si=7Qtftq=7Qtfm=&zdbp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=k-t=2<_Pf=Si=7Rcptq=7Rcpm=(@+bp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=$.'t=2<b!f=Si=7Tnutq=7Tnum=3cSbp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=Hvt=2<f#f=Si=7U;otq=7U;om=%H/bp=#%Aap=#%9," \
#       "p=#%Kop=#%Kq=C3t=2<i>f=Bi=7U^%tq=7U^%m=$t-bp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=\?t=2<p&f=Si=7V=Btq=7V=Bm='**bp=#%Aap=#%9," \
#       "p=#%Kop=#%Kq=%nMt=2<sHf=Bi=7Z/ntq=7Z/nm=A87bp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=#0t=2<w!f=Si=7Z0~tq=7Z0~m=+%bp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=$=t=2<y*f=Si=7Z3<tq=7Z3<m=5(bp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=^Lt=2=#Cf=Si=7Zngtq=7Zngm='3dbp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=Pzt=2=&;f=Si=7\Cetq=7\Cem=&0Dbp=#%Aap=#%9," \
#       "p=#%Aop=#%Kq=LDt=2=+=f=Si=7\o-tq=7\o-m=%e8bp=#%Aap=#%9," \
#       "p=#%Aop=#%Aq=S;t=2=/.f=Si=7^FEtq=7^FEm=&BJbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=Y$t=2=2?f=Si=7_$Gtq=7_$Gm=&qGbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=9~t=2=h?f=Si=7_<Ftq=7_<Fm=$(Pbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq==It=2=kBf=Si=7_Vntq=7_Vnm=$DQbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=g_t=2=oTf=Si=7`BOtq=7`BOm=(#Abp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=#0t=2=tvf=Bi=7`C^tq=7`C^m=+%bp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=-At=2=yrf=Bi=7`N!tq=7`N!m=v>bp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=*&t=2>0_f=Bi=7`V&tq=7`V&m=d3bp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=wgt=2>6)f=Si=7aQktq=7aQkm=)L8bp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=K7t=2>9yf=Si=7b!%tq=7b!%m=%Ykbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq==It=2>A6f=Si=7b=Ltq=7b=Lm=$DQbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=*&t=2>CRf=Si=7bEPtq=7bEPm=d1bp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=;O3t=2B2@f=Si=7zsbtq=7zsbm=$5Lebp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=.Nt=2B4`f=Si=7~%4tq=7~%4m=#%7bp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=3*t=2B>*f=Bi=7~6<tq=7~6<m=#JMbp=#%7ap=#%9," \
#       "p=#%7op=#%Aq=#0t=2B>Lf=Si=7~7Itq=7~7Im=+$bp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=.Nt=2BErf=Bi=7~Bvtq=7~Bvm=#%;bp=#%7ap=#%9," \
#       "p=#%Aop=#%Aq=$=t=2BI?f=Bi=7~E7tq=7~E7m=5(bp=#%7ap=#%9"
#
# decode_quote(str_code)
