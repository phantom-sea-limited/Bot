import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: '用起来简单?',
    Svg: require('../../static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        大概?
      </>
    ),
  },
  {
    title: '专注摸鱼',
    Svg: require('../../static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        没错了
      </>
    ),
  },
  {
    title: '方便扩展?',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        也许是的
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
