using System;

namespace Kampus.Model
{
    public class Kisi
    {
        private readonly string ad;

        public string Ad => ad;

        protected Kisi(string ad)
        {
            if (string.IsNullOrWhiteSpace(ad))
            {
                throw new ArgumentException("Ad alanı boş veya yalnızca boşluklardan oluşamaz.", nameof(ad));
            }

            this.ad = ad.Trim();
        }
    }
}
