from path import  Path
import random
import pandas as pd
import numpy as np
import json

def json2dict(file):
    with open(file, 'r') as f:
        dict = json.load(fp=f)
        return dict

def get_dict_from(stem,instances):
    for idx, item in enumerate( instances):
        if stem == item['stem']:
            return idx,item
    return -1,None

class DataLoader:
    def __init__(self,dir_path):
        self.dir_path = Path(dir_path)
        input_p = self.dir_path/'input.json'
        self.input_tab=None
        if input_p.exists():
            self.input_tab =  json2dict(input_p)

        self.output_tab = self.input_tab


        self.base = Path( self.output_tab['base'])
        # self.metric_df = pd.DataFrame(columns=[  self.output_tab['data_names']])


        self.stems=[]
        for ins in  self.output_tab['instances']:
            self.stems.append(ins['stem'])

    @staticmethod
    def load(dir_path):
        dl = DataLoader(dir_path)
        output_p = Path(dir_path)/'output.json'
        if output_p.exists():
            dl.output_tab = json2dict(output_p)
        return dl

    def get_metric_df(self ,*args ,**kwargs):
        metric = kwargs.get("metric")
        hues = kwargs.get("hues")
        n_sample = kwargs.get("n_sample" ,100)

        options = kwargs.get("options" ,{})

        if (metric=='throughput' or metric=='throughputv2' or metric =="max_throughput") and 'throughput' in self.output_tab['data_names']:
            df_ret = pd.DataFrame()

            for idx, ins in enumerate(self.output_tab['instances']):

                try:
                    if metric =="max_throughput":
                        data_length =1
                        df = pd.DataFrame({
                            "max_throughput": [ins['throughput']['throughput'][-1]]
                        })
                    else:
                        data_length = min(len(ins[metric]['throughput']), len(ins[metric]['loads_list']))
                        df = pd.DataFrame({
                            "loads_list" :ins[metric]['loads_list'][:data_length],
                            "throughput" :ins[metric]['throughput']
                        })

                    _, input_ins = get_dict_from(ins['stem'], self.input_tab['instances'])

                    if hues:
                        for hue in hues:
                            if hue in ins.keys():
                                df[hue] = data_length * [ins[hue]]
                            else:
                                print("{} is not in init instance".format(hue))
                    df_ret = pd.concat([df_ret ,df])

                except:
                    print('error')
                    pass


            return df_ret
        elif metric == 'rtt' and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                try:
                    data_length = min(len(ins[metric]['rtt']), len(ins[metric]['trans_delay_list']))
                    df = pd.DataFrame({
                        "trans_delay_list": ins[metric]['trans_delay_list'][:data_length],
                        "rtt": ins[metric]['rtt']
                    })

                    _, input_ins = get_dict_from(ins['stem'], self.input_tab['instances'])

                    if hues:
                        for hue in hues:
                            if hue in ins.keys():
                                df[hue] = data_length * [ins[hue]]
                            else:
                                print("{} is not in init instance".format(hue))
                    df_ret = pd.concat([df_ret, df], ignore_index=True)

                except:
                    print('ok')

            return df_ret
        elif metric in  ['capacity' ,'time_consumption' ,'time_throughput'] and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                data_length =min(len(ins[metric][metric]),len(ins[metric]['time_stamps']))

                df = pd.DataFrame({
                    "time_stamps": ins[metric]['time_stamps'][:data_length],
                    metric: ins[metric][metric][:data_length]
                })
                if hues:
                    for hue in hues:
                        if hue in ins.keys():
                            df[hue] = data_length * [ins[hue]]
                        else:
                            print("{} is not in init instance".format(hue))
                df_ret = pd.concat([df_ret, df], ignore_index=True)

            return df_ret
        elif metric == 'net-utl' and 'throughput' in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                x_len = len(ins['throughput']['loads_list'])
                try:
                    df = pd.DataFrame({
                        "pattern": x_len * [ins["pattern"]],
                        "phase_factor": x_len * [ins["phase_factor"]],
                        "constellation": x_len * [ins["constellation"]],
                        "duty_ratio": x_len * [ins["duty_ratio"]],
                        "loads_list": ins['throughput']['loads_list'][:x_len],
                        "net-utl": list(np.array(ins['throughput']['throughput'])[:x_len] / ins['capacity'][0] * 100)
                    })
                except:
                    print('ok')
                df_ret = df_ret.append(df)
            return df_ret
        elif metric == 'usr-utl' and 'throughput' in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                x_length = min(len(ins[metric]['throughput']), len(ins[metric]['loads_list']))

                df = pd.DataFrame({
                    "pattern": x_length * [ins["pattern"]],
                    "phase_factor": x_length * [ins["phase_factor"]],
                    "constellation": x_length * [ins["constellation"]],
                    "duty_ratio": x_length * [ins["duty_ratio"]],
                    "loads_list": ins['throughput']['loads_list'],
                    "usr-utl": list(
                        1000 * np.array(ins['throughput']['throughput']) / np.array(ins['throughput']['loads_list']))
                })
                df_ret = df_ret.append(df)
            return df_ret
        elif metric in ['hop-count', 'stretch', 'num_rediscovery', 'reach', 'jitter', 'ISL_loads'] and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                metrics = ins.get(metric, {metric: [0]}).get(metric)
                df = pd.DataFrame({
                    metric: metrics
                })
                data_length = len(metrics)
                if hues:
                    for hue in hues:
                        if hue in ins.keys():
                            df[hue] = data_length * [ins[hue]]
                        else:
                            print("{} is not in init instance".format(hue))
                df_ret = pd.concat([df_ret, df], ignore_index=True)
            return df_ret
        elif metric == 'overhead' and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()
            for idx, ins in enumerate(self.output_tab['instances']):
                df = pd.DataFrame({
                    "time_stamp": ins[metric]['time_stamp'],
                    "fib_freq": ins[metric]['fib_freq'],
                    "ctrlpkt_freq": ins[metric]['ctrlpkt_freq']

                })
                data_length = len(ins[metric]['time_stamp'])
                if hues:
                    for hue in hues:
                        if hue in ins.keys():
                            df[hue] = data_length * [ins[hue]]
                        else:
                            print("{} is not in init instance".format(hue))
                df_ret = pd.concat([df_ret, df], ignore_index=True)
            return df_ret
        elif metric == 'network_change' and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()

            for idx, ins in enumerate(self.output_tab['instances']):
                ins[metric]['network_change'].insert(0,0)
                data_length = len(ins[metric]['network_change'])
                df_dict = {}
                df_dict.update(ins[metric])
                if options.get("blocks", None):
                    df_dict["time_num_blocks"] = ins[metric]['num_blocks'][:data_length],
                    df_dict["time_num_vagrants"] = ins[metric]['num_vagrants'][:data_length],
                    df_dict["time_num_faults"] = ins[metric]['num_faults'][:data_length],
                    df_dict["time_num_non_IBLs"] = ins[metric]['num_non_block_links'][:data_length]
                # df_dict.pop('time_diff_edges')
                df = pd.DataFrame(df_dict)
                if hues:
                    for hue in hues:
                        if hue in ins.keys():
                            df[hue] = data_length * [ins[hue]]
                        else:
                            print("{} is not in init instance".format(hue))
                df_ret = pd.concat([df_ret, df], ignore_index=True)
            return df_ret
        elif metric == 'latency' and metric in self.output_tab['data_names']:
            df_total = pd.DataFrame()
            random.seed(123)
            # selected_idxs = random.sample(list(range(len(self.input_tab['instances']))), n_sample)
            for idx, ins in enumerate(self.output_tab['instances']):
                # if idx not in selected_idxs:continue
                df_ins = pd.DataFrame()
                for traffic_id, src_dst, latency in zip(ins[metric]['traffic_hashId'], ins[metric]['src_dst'],
                                                        ins[metric]['latency']):
                    df_sub = pd.DataFrame({
                        "traffic_hashId": traffic_id * len(ins[metric]['time_stamps']),
                        "time_stamps": ins[metric]['time_stamps'],
                        "src_dst": [src_dst] * len(ins[metric]['time_stamps']),
                        "latency": latency
                    })
                    df_ins = pd.concat([df_ins, df_sub], ignore_index=True)
                data_length = len(df_ins)
                if hues:
                    for hue in hues:
                        if hue in ins.keys():
                            df_ins[hue] = data_length * [ins[hue]]
                        else:
                            print("{} is not in init instance".format(hue))

                df_total = pd.concat([df_total, df_ins], ignore_index=True)
            return df_total
        elif metric in ['isl_cost','availability'] and metric in self.output_tab['data_names']:
            df_ret = pd.DataFrame()

            for idx, ins in enumerate(self.output_tab['instances']):
                metric_dict = self.output_tab['instances'][0].get(metric,{})
                ret_dict={}
                sub_metrics = options.get("sub_metrics",list(metric_dict.keys()))
                for sub_metric in sub_metrics:
                    ret_dict[sub_metric] = ins[metric][sub_metric]
                data_length = len(ins[metric][sub_metrics[0]])

                df = pd.DataFrame(ret_dict)
                if hues:
                    for hue in hues:
                        if hue in ins.keys() and hue != metric: #这里已经将avb的sub-metric弄上去了,所以不必
                            df[hue] = data_length * [ins[hue]]
                        elif hue not in ins.keys() and hue == metric:
                            pass
                        else:
                            print("{} is not in init instance".format(hue))
                df_ret = pd.concat([df_ret, df], ignore_index=True)

            return df_ret

