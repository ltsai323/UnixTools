void DrawAllHists(const char* ifile)
{
   std::string fold="allhists/";

   TFile f(ifile);
   TIter next(f.GetListOfKeys());
   TKey *key;
   TCanvas c1("c","",500,500);
   while ((key = (TKey*)next())) {
      TClass *cl = gROOT->GetClass(key->GetClassName());
      if (!cl->InheritsFrom("TH1")) continue;
      TH1 *h = (TH1*)key->ReadObj();
      std::string name(h->GetName());
      name+=".jpg";
      h->Draw();
      c1.SaveAs( (fold+name).c_str());
   }
}
