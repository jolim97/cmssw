from ROOT import *
import os
import sys
import array
gStyle.SetOptStat(kFALSE)

#fname1 = "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"
fname1 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0__RECO.root"
fname2 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0_pre13__RECO.root"

ZTTdir="DQMData/Run 1/RecoTauV/Run summary/miniAODValidation/ZTT/"
f1 = TFile(fname1)
f2 = TFile(fname2)
dir_antiids = ['vsJet','vsEle','vsMuo']
dir_wps = ['loose','medium','tight']
variables = ['_pt','_eta','_phi','_mass','_pu']
hists={}
c1 = TCanvas('c','c',800, 800)

plotpath = './plots'
if not os.path.isdir(plotpath):
    os.mkdir(plotpath)

for i in dir_antiids:
    for j in dir_wps:
        for k in variables:
            c1.cd()
            h1 = f1.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
            h2 = f2.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
            h1.Scale(1.0/h1.Integral())
            h2.Scale(1.0/h2.Integral())
            if(k=='_eta'or k=='_phi'):
                xbins = array.array('d', [x-4 for x in range(9)])
                h1=h1.Rebin(8,'rebinned',xbins)
                h2=h2.Rebin(8,'rebinned',xbins)
            elif(k=='_pt'):
                xbins = array.array('d', [(y-1)*20 for y in range(12)])
                h1=h1.Rebin(11,'rebinned',xbins)
                h2=h2.Rebin(11,'rebinned',xbins)
            elif(k=='_mass'):
                xbins = array.array('d', [(y-1)*0.2 for y in range(12)])
                h1=h1.Rebin(11,'rebinned',xbins)
                h2=h2.Rebin(11,'rebinned',xbins)
            elif(k=='_pu'):
                xbins = array.array('d', [(y-1)*10 for y in range(12)])
                h1=h1.Rebin(11,'rebinned',xbins)
                h2=h2.Rebin(11,'rebinned',xbins)
            h1.SetMarkerStyle(kFullCircle)
            h1.SetMarkerColor(kRed)
            h1.SetLineColor(kRed)
            gStyle.SetEndErrorSize(2)
            gStyle.SetErrorX(0.)
            h2.SetLineColor(kBlue)
            m = max(h1.GetMaximum(), h2.GetMaximum())
            h1.SetMaximum(m*1.2)
            h1.Draw("err p")
            h2.Draw("hist same")
            leg = TLegend(0.6, 0.8, 0.8, 0.89)
            leg.AddEntry(h1,'CMSSW_11_0_0', 'p')
            leg.AddEntry(h2,'CMSSW_11_0_0_pre13','l')
            leg.SetBorderSize(0)
            leg.SetTextSize(0.025)
            leg.Draw()
            c1.Print('./plots/'+"ZTTtau_"+j+i+k+'CMSSW_11_0_0_vs_CMSSW_11_0_0_pre13.pdf')

