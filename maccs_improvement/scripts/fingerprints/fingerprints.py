"""
Contains a class for fingerprints which can make fingerprints acc. to the lumiaropapers as defaults.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from rdkit.Chem import AllChem
from rdkit.Chem import (MACCSkeys, RDKFingerprint)


class Fingerprints:
    "Default values set from the Lumiaro Paper"
    def __init__(self,
        fp_type = None,
        radius = 2,
        n_bits=2048,
        n_bits_per_hash = 16,
        max_path = 8,
        fp_size = 8192):

        self.fp_type = fp_type
        self.radius = radius
        self.n_bits = n_bits
        self.n_bits_per_hash = n_bits_per_hash
        self.max_path = max_path
        self.fp_size = fp_size

    def get_fingerprint(self,smiles, **kwargs):
        "Takes a SMILES string, converts it to a 2d molecule and outputs a fingerprint"
        try:
            mol = AllChem.MolFromSmiles(smiles)
            if self.fp_type == 'Morgan':
                fingerprint =  AllChem.GetMorganFingerprintAsBitVect(mol, radius =
                    self.radius, n_bits = self.n_bits, **kwargs)
            elif self.fp_type == 'MACCS':
                fingerprint = MACCSkeys.GenMACCSKeys(mol, **kwargs)
            elif self.fp_type == 'topological':
                fingerprint = RDKFingerprint(mol, maxPath = self.max_path,
                                                  nBitsPerHash = self.n_bits_per_hash,
                                                  fpSize = self.fp_size, **kwargs) #Has to be written in uppercase
            elif self.fp_type is None:
                raise Exception('Error: Enter fingerprint type')
        except:
            fingerprint=np.NaN
        return fingerprint

class MACCSAnalysis(pd.DataFrame):
    "Class with custom functions to apply to maccs fingerprints"
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self['MACCS'] = self['SMILES'].apply(lambda x:
            Fingerprints(fp_type='MACCS').get_fingerprint(x) if(np.all(pd.notnull(x)))
            else np.NaN)
        
    def maccs_to_array(self,fp_):
        "Convert maccs string fingerprint to an array"
        try:
            bit_fp = np.frombuffer(fp_.ToBitString().encode(), 'u1') - ord('0')
        except:
            bit_fp = np.NaN
        return bit_fp

    def make_maccs_df(self):
        "return a maccs array with each key as an entry."
        return pd.DataFrame(self['MACCS'].apply(lambda x: self.maccs_to_array(x)
            if(np.all(pd.notnull(x))) else np.NaN).to_list())

    def get_counts(self):
        """Count number of times a feature key appears in a dataset fingerprints
        feature_counts: A count of how often each key appears in dataset, 
        nz_features: The subset of feature_counts (normalized) of only the active features,
        n_shared_features: Vector with features that are active in 0-95% of the dataset, 
        size: Size of analyzed datasets"""
        feature_counts = self.make_maccs_df().sum()
        nz_features = feature_counts[feature_counts != 0]/len(self.make_maccs_df())
        return feature_counts, nz_features

    def shared_features(self, nz_features, percentages):
        "find how many times a feature appears at least X percent"
        n_shared_features=[]
        for i in percentages:
            n_shared_features.append(len(nz_features[nz_features > i]))
        return n_shared_features

    def group_correlated_features(self, nz_features, corr_threshold):
        "Get number of times that features appear together in groups"
        nz_corr = self.make_maccs_df()[nz_features.index.to_list()].corr()
        index_ = nz_corr.where((nz_corr  > corr_threshold), np.NaN) # Remove negative correlation | (nz_corr  < -threshold)?
        corr_features = []
        for i in index_.columns:
            corr_features.append(list(index_[index_.loc[i] > corr_threshold].index))
        return pd.DataFrame([nz_features.index, corr_features], index=['Key','High corr. features']).transpose().set_index('Key')

    def plot_heatmap(self, nz_features, filename, threshold):
        "plot how often features appear together"
        nz_corr = self.make_maccs_df()[nz_features.index.to_list()].corr()
        index_ = nz_corr.where((nz_corr  > threshold) | (nz_corr  < -threshold), np.NaN)
        heatplot = sns.heatmap(index_, cmap="Blues", xticklabels=nz_corr.columns,
            yticklabels=nz_corr.columns)
        fig = heatplot.get_figure()
        fig.savefig(filename+"_heatmap.png")

    def plot_feature_distribution(self, shared_features, nz_features, percentages, filename):
        "Plot how many features appear in more than x percent of dataset"
        cm = 1/2.54
        plt.rc('font', size=10)
        fig, axs = plt.subplots(1,2,dpi=300,figsize=(18.0*cm,7.0*cm))
        fig.subplots_adjust(wspace=0.2, hspace=0.05)
        axs[0].plot(percentages, shared_features, marker='o', markersize=2.5, linewidth=1)
        axs[0].set_ylabel('Number of features')
        axs[1].hist(nz_features, 20,facecolor='b', histtype='bar',rwidth=3.0)
        plt.setp(axs, xlim=[-0.04,1], xlabel = 'Percent of dataset')
        plt.subplots_adjust(bottom=0.15)
        plt.savefig(filename+"_fdist.png",bbox_inches='tight')

    def plot_feature_fp(self, feature_counts, filename):
        "Plot how often the features appear in the dataset"
        cm = 1/2.54
        plt.rc('font', size=10)
        fig, axs  = plt.subplots(figsize=(6.0*cm,4.5*cm),dpi=300)
        axs.bar(np.arange(167),  feature_counts/len(self))
        plt.setp(axs, xlim=[-0.04,166], ylim=[0,1], xlabel = 'MACCS key',
            ylabel='Feature count')
        plt.subplots_adjust(bottom=0.15)
        plt.savefig(filename+"_featurefp.png",dpi=300,bbox_inches='tight')
