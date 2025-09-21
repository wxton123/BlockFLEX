import unittest
from lib import  DataLoader
import seaborn as sns
import random
import matplotlib.pyplot as plt
from pathlib import  Path
route_order = ['MHP', 'SDP', 'OrbitCast', 'SHORT', 'BlockFLEX (w/o OS3)', 'BlockFLEX']

class TestBlockFLEX(unittest.TestCase):

    def setUp(self):
        # 创建输出目录
        self.output_dir = Path("./outputs")
        self.output_dir.mkdir(exist_ok=True)



    '''     EXP1
    '''
    def test_net_numvs_barplot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset1/")
        metric_df = dataloader.get_metric_df(metric='network_change', hues=['constellation','duty_ratio','network'])

        metric_df['avg_deg'] = metric_df['num_non_block_links']/(metric_df['num_blocks'] + metric_df['num_vagrants'])

        fig, ax = plt.subplots(figsize=[3.5, 2.2])
        plt.subplots_adjust(left=0.26, bottom=0.155, right=0.97, top=0.855)


        sns.barplot(metric_df,y='num_vagrants',x='constellation',hue='network',legend=True)
        plt.ylabel('Num. of vagrant\nsatellites',fontsize=14)


        plt.xticks( fontsize=12,ha='right')
        plt.yticks(fontsize=12)
        plt.xlabel(' ')
        plt.yscale('log')


        for index, rect in enumerate(ax.patches):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 0.5,  # 0.5 是垂直偏移量，可能需要根据实际情况调整
                    f'{height:.0f}', ha='center', va='bottom', rotation=0)
        plt.savefig(self.output_dir/"exp1-1.png")
        # plt.show()
    def test_net_avgdeg_barplot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset1/")
        metric_df = dataloader.get_metric_df(metric='network_change', hues=['constellation', 'duty_ratio', 'network'])
        metric_df['avg_deg'] = metric_df['num_non_block_links']/(metric_df['num_blocks'] + metric_df['num_vagrants'])

        fig, ax = plt.subplots(figsize=[3.5, 2.2])
        plt.subplots_adjust(left=0.215, bottom=0.155, right=0.97, top=0.855)

        sns.barplot(metric_df,x='constellation',y='avg_deg',hue='network')

        plt.xticks(fontsize=12, ha='right')
        plt.yticks(fontsize=12)
        plt.ylabel('Avg. degree of FUs',fontsize=14)
        plt.legend(loc='lower right',ncols=2)
        plt.xlabel(' ')
        plt.savefig(self.output_dir/"exp1-2.png")
        # plt.show()

    def test_net_change_cdf_plot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset1/")
        metric_df = dataloader.get_metric_df(metric='network_change', hues=['constellation', 'duty_ratio', 'network'])
        cons = 'StarLink'
        # cons = 'OneWeb'

        metric_df = metric_df.query("constellation == '{}'".format(cons))
        metric_df['network_change']/=10# simulation time delta

        fig, ax = plt.subplots(figsize=[3.5,2.2])
        plt.subplots_adjust(left=0.21, bottom=0.29, right=0.94, top=0.855)
        plt.xticks( fontsize=12, ha='right')
        plt.yticks( fontsize=12, ha='right')

        plt.ylabel('CDF(%)',fontsize=14)
        plt.xlabel('Num. of IULs changes/s',fontsize=14)
        plt.title(cons)

        plt.yticks(fontsize=12)
        sns.ecdfplot(metric_df, x="network_change",hue='network',stat='percent',
                     hue_order=['BASIC','STATIC','RANDOM','CQSBE'],linewidth=2)

        plt.savefig(self.output_dir/"exp1-3.png")
        # plt.show()

    '''     EXP2
    '''

    def test_reach_description_rls(self):


        dataloader = DataLoader.load(dir_path="dataset2/") #reach





        for CONS in ['OneWeb','StarLink']:
            for duty_ratio in ['0.7','0.8','0.9','1']:
                metric_df = dataloader.get_metric_df(metric='reach', hues=['constellation', 'duty_ratio', 'route'])

                metric_df = metric_df.query("constellation == '{}'".format(CONS))

                metric_df = metric_df.query("duty_ratio == {}".format(duty_ratio))

                df = metric_df.groupby('route').describe()
                df.to_csv(self.output_dir/'exp2-1-{}-{}.csv'.format(CONS,duty_ratio))



    '''EXP3
    '''

    def test_num_redis_plot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset2")

        for cons in ['OneWeb','StarLink']:
            metric_df = dataloader.get_metric_df(metric='num_rediscovery',
                                                 hues=['constellation', 'duty_ratio', 'route'])
            metric_df = metric_df.query("constellation == '{}'".format(cons))
            # metric_df = metric_df.query("constellation == 'StarLink'")



            show_route = ['OrbitCast','OrbitCast+nBAS','SHORT','SHORT+nBAS','DABR(CTV)-CQSBE',"DABR(CTV)-CQSBE-nBAS"]#'DABR-MDV-SBE-nBAS',DABR-TNV-SBE-nBAS
            metric_df = metric_df.query("route in {}".format(show_route))
            metric_df.loc[metric_df['route'] == 'SHORT', 'num_rediscovery'] += 0.08 #for plotting
            metric_df.loc[metric_df['route'] == 'OrbitCast', 'num_rediscovery'] += 0.05 #for plotting

            # fig, ax = plt.subplots(figsize=[4, 2.5])#paper
            fig, ax = plt.subplots(figsize=[6, 5])

            plt.subplots_adjust(left=0.190, bottom=0.25, right=0.975, top=0.92)
            sns.lineplot(ax=ax,data=metric_df,
                         hue_order=show_route,
                         style='constellation',
                         markers=True,
                         y="num_rediscovery",x='duty_ratio',hue='route',
                         palette=sns.color_palette(),legend=False)

            plt.ylabel('Num. routing \n re-discovery',fontsize=15)
            plt.yticks([0,1,2,3],fontsize=15)
            plt.ylim([-0.2,3])

            plt.xticks([0.7,0.8,.9,1],['30%','20%','10%','0%'],fontsize=15)
            plt.xlabel("ISL failure ratio",fontsize=15)
            # print(metric_df.groupby('route').describe())


            colors = sns.color_palette()

            labels = ['OrbitCast','OrbitCast+nBAS','SHORT','SHORT+nBAS', 'BlockFlex (w/o nBAS)', 'BlockFlex']
            for i, label in enumerate(labels):
                line = plt.Line2D([0], [0], color=colors[i], lw=2, label=label)
                ax.add_line(line)
            ax.legend(ncols=2)
            plt.savefig(self.output_dir/'exp-3-1-{}.png'.format(cons))
            # plt.show()



    def test_overhead_plot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset3")
        metric_df = dataloader.get_metric_df(metric='overhead', hues=['constellation', 'duty_ratio', 'route'])

        fig, ax = plt.subplots(figsize=[4, 2.5])
        plt.subplots_adjust(left=0.190, bottom=0.1, right=0.975, top=0.92)

        custom_palette = sns.color_palette()



        metric_df.loc[(metric_df['route'] == 'SHORT') & (metric_df['fib_freq'] == 0), 'fib_freq'] += 0.03 #for plot
        metric_df.loc[(metric_df['route'] == 'SHORT') & (metric_df['ctrlpkt_freq'] == 0), 'ctrlpkt_freq'] += 0.03 #for plot
        metric_df.loc[(metric_df['route'] == 'OrbitCast') & (metric_df['fib_freq'] == 0), 'fib_freq'] += 0.03 #for plot
        metric_df.loc[(metric_df['route'] == 'OrbitCast') & (metric_df['ctrlpkt_freq'] == 0), 'ctrlpkt_freq'] += 0.03 #for plot

        #=== control msg ===
        sns.barplot(metric_df, x="duty_ratio",y='ctrlpkt_freq',hue='route',palette=custom_palette)
        plt.ylabel('Num. routing\ncontrol message/s',fontsize=14)

        for index, rect in enumerate(ax.patches):
            height = rect.get_height()
            if index >=3 and index <5:
                ax.text(rect.get_x() + rect.get_width() / 2, height ,  # 0.5 是垂直偏移量，可能需要根据实际情况调整
                    f'{height:.0f}', ha='center', va='bottom', rotation=0)



        plt.xlabel(' ')
        plt.xticks([])
        plt.yticks(fontsize=12)
        plt.legend(title=None,ncols=1,fontsize=12)
        plt.yscale('log')
        print(metric_df.groupby('route').describe()[['ctrlpkt_freq','fib_freq']])

        plt.savefig(self.output_dir/"exp3-2-ctrl-msg.png")

        #  === FIB ===
        fig, ax = plt.subplots(figsize=[4, 2.5])
        plt.subplots_adjust(left=0.190, bottom=0.1, right=0.975, top=0.92)
        sns.barplot(metric_df, x="duty_ratio",y='fib_freq',hue='route',palette=custom_palette,linewidth=2)
        plt.ylabel('Num. FIB updates/s',fontsize=14)

        for index, rect in enumerate(ax.patches):
            height = rect.get_height()
            if index >=3 and index <5:
                ax.text(rect.get_x() + rect.get_width() / 2, height ,  # 0.5 是垂直偏移量，可能需要根据实际情况调整
                    f'{height:.0f}', ha='center', va='bottom', rotation=0)



        plt.xlabel(' ')
        plt.xticks([])
        plt.yticks(fontsize=12)
        plt.legend(title=None,ncols=1,fontsize=12)
        plt.yscale('log')

        plt.savefig(self.output_dir/"exp3-2-fib.png")

        # plt.show()



    ''' EXP4
    '''
    def test_consumption_plot(self):


        custom_palette = sns.color_palette()

        dataloader = DataLoader.load(dir_path="dataset4")

        metric_df = dataloader.get_metric_df(metric='time_consumption', hues=['constellation', 'duty_ratio', 'route'])
        metric_df['time_consumption']*=1000# sec-to-ms


        fig, ax = plt.subplots(figsize=[4, 3])#single-c
        plt.subplots_adjust(left=0.24, right=0.95,bottom=0.21,top=0.92)


        #line plot
        sns.lineplot(metric_df,x='time_stamps',y='time_consumption',hue='route',linewidth=2,legend=True,palette=custom_palette)
        plt.xticks(fontsize=14)
        plt.ylabel("Time consumption \n per dataflow (ms)", fontsize=14)
        plt.xlabel("Time elapsed (Sec)", fontsize=14)
        plt.legend(title=None,fontsize=13)
        plt.yticks(fontsize=14)
        print(metric_df.groupby('route').describe()['time_consumption'])
        plt.savefig(self.output_dir/"exp4-1.png")


        # cdf plot
        plt.subplots_adjust(left=0.195, right=0.90,bottom=0.21)
        sns.ecdfplot(metric_df,x='time_consumption',hue='route',linewidth=2,stat='percent',legend=False,palette=custom_palette)
        plt.xlabel("Time consumption per dataflow (ms)", fontsize=14)
        plt.ylabel("CDF(%)", fontsize=14)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.savefig(self.output_dir/"exp4-2.png")
        # plt.show()


    ''' EXP5
    '''

    def test_global_latency_barplot_rls(self):

        custom_palette = sns.color_palette()


        dataloader = DataLoader.load(dir_path="dataset5")

        metric_df = dataloader.get_metric_df(metric='stretch', hues=['constellation', 'duty_ratio', 'route'])


        fig, ax = plt.subplots(figsize=[8, 5])#dc


        plt.subplots_adjust(left=0.205, right=0.95,bottom=0.21)

        sns.barplot(metric_df, y="stretch", x='constellation',hue='route',
                    linewidth=2,
                    legend=True,palette=custom_palette,hue_order = route_order

        )
        plt.ylim([0,4])



        plt.xticks( fontsize=24)
        plt.xlabel(None)
        plt.ylabel("Path stretch \n (normalized latency)",fontsize=24)
        plt.yticks([0,1.5,3,4.5],fontsize=24)
        plt.legend(title=None,ncol=3,fontsize=12)

        plt.savefig(self.output_dir/"exp-4-1.png")

        # plt.show()

    def test_global_jitter_plot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset5")

        metric_df = dataloader.get_metric_df(metric='jitter', hues=['constellation', 'duty_ratio', 'route'])
        fig, ax = plt.subplots(figsize=[8, 5])#dc


        plt.subplots_adjust(left=0.205, right=0.95,bottom=0.21)
        plt.ylim(0,35)

        custom_palette = sns.color_palette()


        plt.yticks([0,10,20,30],fontsize=24)
        sns.barplot(metric_df,x='constellation',y='jitter',hue='route',palette=custom_palette,
                    legend=False,
                    hue_order=route_order
                    )
        plt.xticks( fontsize=24,ha='right')

        plt.ylabel("Latency jitter (ms)", fontsize=24)
        plt.xlabel(' ')
        plt.xticks(None)
        plt.savefig(self.output_dir/"exp-4-2.png")
        # plt.show()

    def test_global_latency_ecdfplot(self):
        route_order = ['MHP', 'SDP', 'OrbitCast', 'SHORT', 'BlockFLEX (w/o OS3)', 'BlockFLEX']

        dataloader = DataLoader.load(dir_path="dataset5")

        metric_df = dataloader.get_metric_df(metric='stretch', hues=['constellation', 'duty_ratio', 'route'])
        metric_df = metric_df.query("duty_ratio == 0.7")

        # metric_df = metric_df.query("constellation == 'OneWeb'")
        metric_df = metric_df.query("constellation == 'StarLink'")

        metric_df = metric_df.sort_values(by='route', ascending=True)
        fig, ax = plt.subplots(figsize=[4, 2.5])
        plt.subplots_adjust(left=0.205, right=0.95, bottom=0.21)
        sns.ecdfplot(metric_df, x="stretch", hue='route', stat='percent', linewidth=2,
                     hue_order=route_order, legend=True,
                     )
        # sns.barplot(metric_df, x="stretch", hue='route',  linewidth=2,
        #              hue_order=['SPR', 'GEOR', 'GEOR-nBAS', 'GEOR-nBAS-CSGI', 'DABR']
        #              )
        # sns.lineplot(metric_df,hue='route')
        # plt.legend(labels=['SPR','GEOR','DABR (w/o L2S3)','DABR'],ncol=5,loc='lower right')

        plt.xticks(fontsize=12)
        plt.xlabel("Stretch (normalized latency)", fontsize=14)
        plt.ylabel("CDF(%)", fontsize=14)
        # ax.axvline(x=1.5,linestyle='--')
        # plt.legend().set_visible(False)
        plt.yticks(fontsize=14)
        plt.savefig(self.output_dir/"exp-4-3.png")
        # plt.show()

    ''' EXP5
    '''
    def test_local_latency_bar_plot_rls(self):


        dataloader = DataLoader.load(dir_path="dataset6")

        metric_df = dataloader.get_metric_df(metric='latency',  hues=['route','duty_ratio','constellation'],n_sample=5)

        custom_palette = sns.color_palette()
        tmp = custom_palette[3]
        custom_palette[3] = custom_palette[5]
        custom_palette[5] = tmp

        end2ends = metric_df['src_dst'].unique()
        random.seed(123)
        sub_end2ends = random.choices(end2ends,k=8)
        sub_end2ends=['London<->Tokyo','Sanya<->Kashi','Sydney<->Moscow','Singapore<->San Fransisco']+sub_end2ends
        metric_df = metric_df.query("src_dst in {}".format(sub_end2ends))

        fig, ax = plt.subplots(figsize=[8, 3])  # single c
        plt.subplots_adjust(left=0.12, right=0.95, bottom=0.31, top=0.9)
        plt.ylabel("One-way latency (ms)",fontsize=15)
        plt.yticks(fontsize=14)
        sns.barplot(metric_df,x='src_dst',y='latency',hue='route',legend=True,palette=custom_palette,
                    hue_order=route_order
                    )
        plt.xticks(rotation=15, fontsize=12,ha='right')
        plt.legend(title=None,ncols=3)
        plt.ylim([0,600])
        plt.xlabel(None)
        plt.savefig(self.output_dir/"exp5-1.png")
        # plt.show()

    def test_local_lat_lineplot_rls(self):
        dataloader = DataLoader.load(dir_path="dataset5")

        custom_palette = sns.color_palette()
        tmp = custom_palette[3]
        custom_palette[3] = custom_palette[5]
        custom_palette[5] = tmp
        idx=0
        metric_df = dataloader.get_metric_df(metric='latency', hues=['route', 'duty_ratio', 'constellation'],n_sample=10)
        e2es = list(metric_df['src_dst'].unique())

        for net_avb_ratio in [0.7,1]:
            for cons in ['OneWeb','StarLink']:
                for e2e in e2es:

                    metric_df = dataloader.get_metric_df(metric='latency', hues=['route', 'duty_ratio', 'constellation'],n_sample=10)

                    metric_df = metric_df.query("duty_ratio == {}".format(net_avb_ratio))
                    metric_df = metric_df.query("constellation == '{}'".format(cons))
                    metric_df = metric_df.query("src_dst  in {}".format([e2e]))
                    # if metric_df==None:
                    #     continue
                    fig, ax = plt.subplots(figsize=[8, 2.6])#single c
                    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.215,top=0.9)

                    sns.lineplot(metric_df, x="time_stamps", y='latency', hue='route',
                                 legend=True,
                                 hue_order=route_order,
                                 palette=custom_palette,
                                 linewidth=2)

                    plt.ylabel("One-way latency (ms)", fontsize=15)
                    plt.yticks(fontsize=14)
                    plt.xlabel("Time elapsed (sec)", fontsize=15)
                    plt.xticks(fontsize=14)
                    plt.title("{},avb:{},src - dst: {}".format(cons,net_avb_ratio,e2e))
                    plt.legend(title='',ncol=3)
                    plt.savefig(self.output_dir/"exp5-2-{}.png".format(idx))
                    idx+=1



if __name__ == '__main__':
    unittest.main()