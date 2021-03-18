from ROOT import *
import os
import sys
import array

def draw2Dhist(hist,cmssw,name):
    c1 = TCanvas('c','c',800, 800)
    c1.cd()
    gStyle.SetPalette(57)
    hist.Draw('COLZ')
    c1.Print('./plots/ZTTtau_'+name+'_'+cmssw+'.pdf')
    c1.Close()

def compare1Dhist(h1,h2,cmssw1,cmssw2,name,binlist):
    c1 = TCanvas('c','c',800, 800)
    h1.Scale(1.0/h1.Integral())
    h2.Scale(1.0/h2.Integral())
    if binlist != None:
        xbins = array.array('d', binlist)
        nbins=len(binlist)-1
        h1=h1.Rebin(nbins,'rebinned',xbins)
        h2=h2.Rebin(nbins,'rebinned',xbins)
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
    leg.AddEntry(h1,cmssw1,'p')
    leg.AddEntry(h2,cmssw2,'l')
    leg.SetBorderSize(0)
    leg.SetTextSize(0.025)
    leg.Draw()
    c1.Print('./plots/'+"ZTTtau_"+name+cmssw1+'_vs_'+cmssw2+'.pdf')
    c1.Close()

gStyle.SetOptStat(kFALSE)

#fname1 = "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"
cmssw1='CMSSW_11_0_0'
cmssw2='CMSSW_11_0_0_pre13'
fname1 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0__RECO.root"
fname2 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0_pre13__RECO.root"

ZTTdir="DQMData/Run 1/RecoTauV/Run summary/miniAODValidation/ZTT/"
f1 = TFile(fname1)
f2 = TFile(fname2)
folders = ['Summary','vsJet','vsEle','vsMuo']
dir_wps = ['loose','medium','tight']
variables2d = ['dmMigration','ntau_vs_dm','pTOverProng_dm0','pTOverProng_dm1','pTOverProng_dm10','pTOverProng_dm11','pTOverProng_dm2']
variables1d1 = ['tau_byDeepTau2017v2p1VSeraw','tau_byDeepTau2017v2p1VSjetraw','tau_byDeepTau2017v2p1VSmuraw','tau_eta','tau_mass','tau_phi','tau_pt','tau_pu']
variables1d2 = ['_pt','_eta','_phi','_mass','_pu']

plotpath = './plots'
if not os.path.isdir(plotpath):
    os.mkdir(plotpath)
for i in folders:
    if(i=="Summary"):
        for j1 in variables2d:
            print("\nDrawing %s"%(ZTTdir+i+'/'+j1))
            h1 = f1.Get(ZTTdir+i+'/'+j1)
            draw2Dhist(h1,cmssw1,j1)
            h2 = f2.Get(ZTTdir+i+'/'+j1)
            draw2Dhist(h2,cmssw2,j1)

        for j2 in variables1d1:
            print("\nDrawing %s"%(ZTTdir+i+'/'+j2))
            h1 = f1.Get(ZTTdir+i+'/'+j2)
            h2 = f2.Get(ZTTdir+i+'/'+j2)
            compare1Dhist(h1,h2,cmssw1,cmssw2,j2,None)
    
    else:
        for j in dir_wps:
            for k in variables1d2:
                print("\nDrawing %s"%(ZTTdir+i+'/'+j+'/tau_'+j+i+k))
                h1 = f1.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
                h2 = f2.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
                bins=None
                if(k=='_eta'or k=='_phi'):
                    bins = [x-4 for x in range(9)]
                elif(k=='_pt'):
                    bins = [(x-1)*20 for x in range(12)]
                elif(k=='_mass'):
                    bins = [(x-1)*0.2 for x in range(12)]
                elif(k=='_pu'):
                    bins = [(x-1)*10 for x in range(12)]
                compare1Dhist(h1,h2,cmssw1,cmssw2,j+i+k,bins)
