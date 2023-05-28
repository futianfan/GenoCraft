import os
import math
import numpy as np
from tqdm import tqdm
## TODO: auto install sklearn or write our own standarscaler
from sklearn.preprocessing import StandardScaler
import networkx as nx
import matplotlib.pyplot as plt


significant_gene_file = 'significant_gene.txt' 
case_file = 'case0.txt'
control_file = 'control0.txt'
output_file = 'output.txt'

class DDN:
    def __init__(self):
        print("DDN package")
    
    def readGeneName(self, filename):
        with open(filename, 'r') as file:
            genename = file.read().split('\n')
        while len(genename) > 0 and genename[-1] == '':
            genename.pop()
        return genename
    
    def readGeneData(self, filename):
        genedata = np.loadtxt(filename)
        genedata = genedata.transpose()
        return genedata
    
    def standardizeGeneData(self, genedata, scaler='rms', zero_mean=True):
        # sample standardization : z = (x - u) / s
        
        standarddata = np.zeros(genedata.shape)
        for i in range(genedata.shape[1]):
            # mean value
            u = np.mean(genedata[:, i]) if not zero_mean else 0
            
            if scaler == 'std':
                # standard deviation
                s = np.std(genedata[:, i])
            elif scaler == 'rms':
                # root mean square
                s = np.sqrt(np.mean(np.square(genedata[:, i])))
            else:
                s = 1
            
            standarddata[:, i] = (genedata[:, i] - u) / s
        
        return standarddata
    
    def concatenateGeneData(self, controldata, casedata, method='diag'):
        if method == 'row':
            return np.concatenate((controldata, casedata), axis=0)
        elif method == 'col':
            return np.concatenate((controldata, casedata), axis=1)
        elif method == 'diag':
            return np.concatenate((np.concatenate((controldata, casedata * 0), axis=0), 
                                   np.concatenate((controldata * 0 ,casedata), axis=0)), axis=1)
        else:
            return []
    
    def solve2d(self, rho1, rho2, lambda1, lambda2):
        """
        description
        
        input
        output:
        cite: 
        
        """
        
        # initialize output
        area_index = 0
        beta1 = 0
        beta2 = 0
        
        if (rho2 <= (rho1 + 2*lambda2) and rho2 >= (rho2 - 2*lambda2) and rho2 >= (2*lambda1 - rho1)):
            area_index = 1
            beta1 = (rho1 + rho2)/2 - lambda1
            beta2 = (rho1 + rho2)/2 - lambda1
        if (rho2 > (rho1 + 2*lambda2) and rho1 >= (lambda1 - lambda2)):
            area_index = 2
            beta1 = rho1 - lambda1 + lambda2
            beta2 = rho2 - lambda1 - lambda2
        if (rho1 < (lambda1 - lambda2) and rho1 >= -(lambda1 + lambda2) and rho2 >= (lambda1 + lambda2)):
            area_index = 3
            beta1 = 0
            beta2 = rho2 - lambda1 - lambda2
        if (rho1 < -(lambda1 + lambda2) and rho2 >= (lambda1 + lambda2)):
            area_index = 4
            beta1 = rho1 + lambda1 + lambda2
            beta2 = rho2 - lambda1 - lambda2
        if (rho1 < -(lambda1 + lambda2) and rho2 < (lambda1 + lambda2) and rho2 >= -(lambda1 + lambda2)):
            area_index = 5
            beta1 = rho1 + lambda1 + lambda2
            beta2 = 0
        if (rho2 < -(lambda1 - lambda2) and rho2 >= (rho1 + 2*lambda2)):
            area_index = 6
            beta1 = rho1 + lambda1 + lambda2
            beta2 = rho2 + lambda1 - lambda2
        if (rho2 >= (rho1 - 2*lambda2) and rho2 < (rho1 + 2*lambda2) and rho2 <= (-2*lambda1 - rho1)):
            area_index = 7
            beta1 = (rho1 + rho2)/2 + lambda1
            beta2 = (rho1 + rho2)/2 + lambda1
        if (rho2 < (rho1 - 2*lambda2) and rho1 <= -(lambda1 - lambda2)):
            area_index = 8
            beta1 = rho1 + lambda1 - lambda2
            beta2 = rho2 + lambda1 + lambda2
        if (rho1 <= (lambda1 + lambda2) and rho1 >= -(lambda1 - lambda2) and rho2 <= -(lambda1 + lambda2)):
            area_index = 9
            beta1 = 0
            beta2 = rho2 + lambda1 + lambda2
        if (rho1 > (lambda1 + lambda2) and rho2 <= -(lambda1 + lambda2)):
            area_index = 10
            beta1 = rho1 - lambda1 - lambda2
            beta2 = rho2 + lambda1 + lambda2
        if (rho2 > -(lambda1 + lambda2) and rho2 <= (lambda1 - lambda2) and rho1 >= (lambda1 + lambda2)):
            area_index = 11
            beta1 = rho1 - lambda1 - lambda2
            beta2 = 0
        if (rho2 > (lambda1 - lambda2) and rho2 < (rho1 - 2*lambda2)):
            area_index = 12
            beta1 = rho1 - lambda1 - lambda2
            beta2 = rho2 - lambda1 + lambda2
        
        return [beta1, beta2]
    
    def bcd(self, y, X, lambda1, lambda2, n1=1, n2=1, threshold=1e-6):
        """
        description
        
        input:
        output:
        cite: 
        
        """
        
        # total feature size must be even
        if (X.shape[1] == 0 or X.shape[1] % 2 == 1):
            return []
        
        # feature size (gene size) for each group
        # x1 (control): feature 0 to p-1
        # x2 (case): feature p to 2*p-1
        p = X.shape[1] // 2
        
        # initialize beta
        beta = np.zeros(2 * p)
        
        if (p == 1):
            rho1 = np.sum(y * X[:, 0]) / n1
            rho2 = np.sum(y * X[:, 1]) / n2
            
            beta2d = self.solve2d(rho1, rho2, lambda1, lambda2)
            beta[0] = beta2d[0]
            beta[1] = beta2d[1]
            
            return beta
        else:
            while (True):
                beta_old = np.copy(beta)
                
                for k in range(p):
                    x1 = X[:, k]
                    x2 = X[:, k + p]
                    
                    idx = [i for i in range(2 * p) if i not in (k, k + p)]
                    y_residual = y - np.dot(X[:, idx], beta[idx])
                    
                    rho1 = np.sum(y_residual * x1) / n1
                    rho2 = np.sum(y_residual * x2) / n2
                    
                    beta2d = self.solve2d(rho1, rho2, lambda1, lambda2)
                    
                    beta[k] = beta2d[0]
                    beta[k + p] = beta2d[1]
                
                if (np.mean(np.abs(beta - beta_old)) < threshold):
                    break
            
            return beta
    
    def generateDifferentialNetwork(self, case_data, control_data, genename, lambda1=0.30, lambda2=0.10, threshold=1e-6):
        # feature size (gene size)
        p = control_data.shape[1]
        
        # sample size
        n1 = control_data.shape[0]
        n2 = case_data.shape[0]
        
        # start calculations
        diffedges = {}
        for gene in tqdm(range(p)):
            # choose one gene as target
            y = self.concatenateGeneData(control_data[:, gene], case_data[:, gene], method='row')
            
            # choose other genes as feature
            idx = [i for i in range(p) if i != gene]
            X = self.concatenateGeneData(control_data[:, idx], case_data[:, idx], method='diag')
            
            # perform bcd algorithm
            beta = self.bcd(y, X, lambda1, lambda2, n1, n2, threshold)
            
            # reindex the features
            beta1 = list(beta[0 : gene]) + [0] + list(beta[gene : p - 1])
            beta1 = np.array(beta1)
            beta2 = list(beta[p - 1 : gene + p - 1]) + [0] + list(beta[gene + p - 1 : 2 * p - 2])
            beta2 = np.array(beta2)
            
            # construct neighbours under two conditions
            condition1 = [genename[i] for i in range(p) if beta1[i] != 0 and beta2[i] == 0]
            condition2 = [genename[i] for i in range(p) if beta2[i] != 0 and beta1[i] == 0]
            weight1 = [beta1[i] for i in range(p) if beta1[i] != 0 and beta2[i] == 0]
            weight2 = [beta2[i] for i in range(p) if beta2[i] != 0 and beta1[i] == 0]
            
            # update results
            for neighbors, weights, condition in zip([condition1, condition2], [weight1, weight2], ['condition1', 'condition2']):
                for neighbor, weight in zip(neighbors, weights):
                    tuple_diffedge = (min(genename[gene], neighbor), max(genename[gene], neighbor), condition)
                    diffedges.setdefault(tuple_diffedge, 0.0)
                    diffedges[tuple_diffedge] += weight
        
        diffedges = sorted([k + tuple([v]) for k, v in diffedges.items()])
        
        return diffedges
    
    def plotDifferentialNetwork(self,diffedges, maxalpha=1.0, minalpha=0.2):
        G = nx.Graph()
        color_condition = {'condition1': [1, 0, 0], 'condition2': [0, 0, 1]}
        maxbeta = max([beta for _, _, _, beta in diffedges])
        
        for gene1, gene2, condition, beta in diffedges:
            if condition in color_condition:
                alpha = beta / maxbeta * (maxalpha - minalpha) + minalpha
                color = list(1 - (1 - np.array(color_condition[condition])) * alpha)
                G.add_edge(gene1, gene2, color=color)
        
        pos = nx.circular_layout(G)
        edges = G.edges()
        edge_color = [G[u][v]['color'] for u, v in edges]
        node_size = [d * 200 for n, d in G.degree()]
        
        fig, ax = plt.subplots(figsize=(6, 6))
        nx.draw(G, pos=pos, node_color='lightblue', node_size=node_size, \
                edgelist=edges, edge_color=edge_color, width=3.5, \
                with_labels=True, font_size=16, font_weight='bold', font_color='magenta')
        
        ax.set_xlim((-1.2, +1.2))
        ax.set_ylim(ax.get_xlim())
        ax.set_title(''.join([
            'DDN Network\n', 
            '\n', 
            'condition #1: red edge\n', 
            'condition #2: blue edge'
        ]))
        plt.show()
    
    def printDifferentialNetwork(self, diffedges, filename=''):
        if len(filename) == 0:
            for gene, neighbor, condition, weight in diffedges:
                print(f"{gene},{neighbor},{condition},{weight}")
        else:
            with open(filename, 'w') as file:
                for gene, neighbor, condition, weight in diffedges:
                    file.write(f"{gene},{neighbor},{condition},{weight}\r")
    
    def DDNPipline(self, case_data_file, control_data_file, gene_name_file, output_file='', lambda1=0.30, lambda2=0.10):
        # import case data
        casedata = self.readGeneData(case_data_file)
        
        # import control data
        controldata = self.readGeneData(control_data_file)
        
        # import gene name
        genename = self.readGeneName(gene_name_file)
        
        # feature size must be equivalent
        assert(casedata.shape[1] == controldata.shape[1])
        
        # feature standardization
        case_standard = self.standardizeGeneData(casedata)
        control_standard = self.standardizeGeneData(controldata)
        
        # generate differential network
        diffedges = self.generateDifferentialNetwork(case_standard, control_standard, genename, lambda1, lambda2)
        
        # print differential network
        self.printDifferentialNetwork(diffedges, output_file)
        
        return diffedges
    
    def DDNBatchPipline(self, path='.', \
                        case_data_suffix='_case.txt', \
                        control_data_suffix='_control.txt', \
                        gene_name_suffix='_genename.txt', \
                        output_suffix='_differential_network.csv', \
                        lambda1=0.30, lambda2=0.10):
        idx = 0
        for file in os.listdir(path):
            if file.endswith(gene_name_suffix):
                gene_name_file = os.path.join(path, file)
                
                prefix = file[:-len(gene_name_suffix)]
                case_data_file = os.path.join(path, prefix+case_data_suffix)
                control_data_file = os.path.join(path, prefix+control_data_suffix)
                output_file = os.path.join(path, prefix+output_suffix)
                
                if os.path.exists(case_data_file) and os.path.exists(control_data_file):
                    self.DDNPipline(case_data_file, control_data_file, \
                                    gene_name_file, output_file, lambda1, lambda2)
                    
                    idx += 1
                    print(f"Dataset#{idx} : {prefix}    successfully processed!")
                
        return


ddn = DDN()
neighbors = ddn.DDNPipline(case_data_file=case_file, \
                           control_data_file=control_file, \
                           gene_name_file=significant_gene_file, \
                           output_file=output_file, \
                           lambda1=0.20, lambda2=0.03)

# exit() 

# beta (704,)
beta1, beta2 = beta[:p], beta[p:]
### original network 1
original_1 = [[1 if (beta1[i]!=0 and beta1[j]==0) or (beta1[i]==0 and beta1[j]!=0) else 0 for j in range(p)] for i in range(p)]

### original network 2 
original_2 = [[1 if (beta2[i]!=0 and beta2[j]==0) or (beta2[i]==0 and beta2[j]!=0) else 0 for j in range(p)] for i in range(p)]

### common network
common_network = [] 
for i in range(p):
    for j in range(i+1,p):
        if original_1[i][j] == 1 and original_2[i][j] == 1:
            common_network.append((i,j)) 

### different network 
different_network = [] 
for i in range(p):
    for j in range(i+1,p):
        if original_1[i][j] + original_2[i][j] == 1:
            different_network.append((i,j))




